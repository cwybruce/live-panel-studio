#!/usr/bin/env python3
"""Local demo gallery with a single queued video exporter; binds 127.0.0.1 only."""
from __future__ import annotations

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import logging
from pathlib import Path
import queue
import re
import threading
from urllib.parse import unquote, urlsplit
import uuid

from export_demo import DEMO_ROOT, ExportError, export, validate_request

BODY_LIMIT = 16 * 1024
UUID_PATTERN = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
JOB_PATH = re.compile(r'^/api/exports/(' + UUID_PATTERN + r')$')
VIDEO_PATH = re.compile(r'^/exports/(' + UUID_PATTERN + r')\.mp4$')


class ExportQueue:
    def __init__(self, demo_root: Path):
        self.root = demo_root.resolve()
        self.jobs = {}
        self.lock = threading.Lock()
        self.pending = queue.Queue(maxsize=16)
        self.worker = threading.Thread(target=self._work, name='live-panel-export', daemon=True)
        self.worker.start()

    def add(self, payload):
        spec = validate_request(payload, self.root)
        identity = str(uuid.uuid4())
        job = {'id': identity, 'status': 'queued', 'progress': 0,
               'scene': spec.scene, 'theme': spec.theme, 'style': spec.style, 'avatar': spec.avatar, 'view': spec.view,
               'filename': spec.filename, 'width': spec.width, 'height': spec.height,
               'fps': 30, 'duration': 12}
        with self.lock:
            if self.pending.full():
                raise queue.Full
            self.jobs[identity] = job
            self.pending.put_nowait((identity, spec))
            return dict(job)

    def get(self, identity):
        with self.lock:
            job = self.jobs.get(identity)
            return dict(job) if job else None

    def _update(self, identity, **changes):
        with self.lock:
            self.jobs[identity].update(changes)

    def _work(self):
        while True:
            identity, spec = self.pending.get()
            self._update(identity, status='running', progress=1, stage='正在准备导出')
            output = self.root / 'exports' / (identity + '.mp4')
            try:
                def progress(value, stage):
                    self._update(identity, progress=round(value, 1), stage=stage)
                info = export(spec, output, progress)
                self._update(identity, status='complete', progress=100, stage='导出完成',
                             url='/exports/' + identity + '.mp4', **info)
            except Exception as error:
                logging.exception('Motion Diagram Studio export %s failed', identity)
                message = '视频生成失败，请重试；详细原因已记录到本地服务日志。'
                if isinstance(error, ExportError) and 'not found' in str(error):
                    message = '未找到导出所需的浏览器或 FFmpeg，请检查本地环境。'
                elif isinstance(error, ExportError) and '超时' in str(error):
                    message = '视频导出超时，请稍后重试。'
                self._update(identity, status='failed', stage='导出失败',
                             error=message)
            finally:
                self.pending.task_done()


class PreviewHandler(SimpleHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'

    def __init__(self, *args, directory, exports, **kwargs):
        self.exports = exports
        super().__init__(*args, directory=str(directory), **kwargs)

    def setup(self):
        super().setup()
        self.connection.settimeout(15)

    def _same_origin(self):
        port = self.server.server_port
        if len(self.headers.get_all('Host', [])) != 1:
            return False
        host = self.headers.get('Host', '').lower()
        allowed = {f'127.0.0.1:{port}', f'localhost:{port}'}
        if port == 80:
            allowed |= {'127.0.0.1', 'localhost'}
        if self.client_address[0] != '127.0.0.1' or host not in allowed:
            return False
        site = self.headers.get('Sec-Fetch-Site')
        if site and site not in ('same-origin', 'none'):
            return False
        origin = self.headers.get('Origin')
        if origin is None:
            return True
        try:
            parsed = urlsplit(origin)
        except ValueError:
            return False
        return parsed.scheme == 'http' and parsed.netloc.lower() == host and not parsed.path and not parsed.query and not parsed.fragment

    def _json(self, status, data):
        blob = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(blob)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.end_headers()
        if self.command != 'HEAD':
            self.wfile.write(blob)

    def _guard(self):
        if not self._same_origin():
            self._json(403, {'error': '仅允许本地预览页面发起请求。'})
            return False
        return True

    def _request_path(self):
        if not self.path.startswith('/') or self.path.startswith('//'):
            raise ValueError('请求路径无效。')
        path = unquote(urlsplit(self.path).path, errors='strict')
        if ('%' in path or '\\' in path or path.startswith('//')
                or any(ord(ch) < 32 or ord(ch) == 127 for ch in path)):
            raise ValueError('请求路径包含歧义编码。')
        return path

    def do_POST(self):
        if not self._guard():
            self.close_connection = True
            return
        try:
            path = self._request_path()
        except (ValueError, UnicodeError):
            self._json(400, {'error': '请求路径无效。'})
            self.close_connection = True
            return
        if path != '/api/exports':
            self._json(404, {'error': '接口不存在。'})
            self.close_connection = True
            return
        if self.headers.get('Transfer-Encoding'):
            self._json(400, {'error': '不支持分块请求。'})
            self.close_connection = True
            return
        if len(self.headers.get_all('Content-Length', [])) != 1:
            self._json(411, {'error': '请求缺少唯一的有效长度。'})
            self.close_connection = True
            return
        try:
            size = int(self.headers.get('Content-Length', ''))
        except ValueError:
            self._json(411, {'error': '请求缺少有效长度。'})
            self.close_connection = True
            return
        if size > BODY_LIMIT:
            self._json(413, {'error': '请求超过 16 KiB 限制。'})
            self.close_connection = True
            return
        if size <= 0 or self.headers.get_content_type() != 'application/json':
            self._json(400, {'error': '请提交有效的 JSON 请求。'})
            self.close_connection = True
            return
        try:
            raw = self.rfile.read(size)
            if len(raw) != size:
                raise ValueError('请求内容不完整。')
            payload = json.loads(raw.decode('utf-8'))
            job = self.exports.add(payload)
        except queue.Full:
            self._json(429, {'error': '导出队列已满，请稍后重试。'})
            return
        except ValueError as error:
            self._json(400, {'error': str(error)[:1000]})
            return
        except Exception:
            logging.exception('Unable to prepare Motion Diagram Studio export')
            self._json(500, {'error': '无法读取本地示例配置，请检查预览服务日志。'})
            return
        self._json(202, job)

    def do_GET(self):
        if not self._guard():
            return
        try:
            path = self._request_path()
        except (ValueError, UnicodeError):
            self._json(400, {'error': '请求路径无效。'})
            return
        if path == '/api/health':
            self._json(200, {'service': 'live-panel-preview', 'exports': True})
            return
        hit = JOB_PATH.fullmatch(path)
        if hit:
            job = self.exports.get(hit.group(1))
            self._json(200 if job else 404, job or {'error': '导出任务不存在。'})
            return
        if path.startswith('/api/'):
            self._json(404, {'error': '接口不存在。'})
            return
        if path.startswith('/exports'):
            hit = VIDEO_PATH.fullmatch(path)
            job = self.exports.get(hit.group(1)) if hit else None
            if not job or job['status'] != 'complete':
                self._json(404, {'error': '导出文件尚未完成或不存在。'})
                return
        if any(part.startswith('.') for part in path.split('/') if part):
            self._json(404, {'error': '文件不存在。'})
            return
        if self.command == 'HEAD':
            super().do_HEAD()
        else:
            super().do_GET()

    def do_HEAD(self):
        if not self._guard():
            return
        try:
            path = self._request_path()
        except (ValueError, UnicodeError):
            self._json(400, {'error': '请求路径无效。'})
            return
        if path.startswith('/api/') or path.startswith('/exports'):
            self.do_GET()
            return
        if any(part.startswith('.') for part in path.split('/') if part):
            self._json(404, {'error': '文件不存在。'})
            return
        super().do_HEAD()

    def do_OPTIONS(self):
        if self._guard():
            self._json(405, {'error': '不支持跨站请求。'})

    def end_headers(self):
        try:
            hit = VIDEO_PATH.fullmatch(self._request_path())
        except (ValueError, UnicodeError):
            hit = None
        if hit:
            job = self.exports.get(hit.group(1))
            if job and job['status'] == 'complete':
                self.send_header('Content-Disposition', 'attachment; filename="' + job['filename'] + '"')
        self.send_header('X-Content-Type-Options', 'nosniff')
        super().end_headers()

    def translate_path(self, path):
        root = Path(self.directory).resolve()
        target = Path(super().translate_path(path)).resolve()
        return str(target if target.is_relative_to(root) else root / '.unavailable')

    def list_directory(self, path):
        self.send_error(404, 'Directory listing is disabled')
        return None


def make_server(port=8779, directory=DEMO_ROOT):
    directory = Path(directory).resolve()
    if not (directory / 'manifest.json').is_file() or not (directory / 'index.html').is_file():
        raise ValueError('预览目录缺少 manifest.json 或 index.html。')
    exports = ExportQueue(directory)
    handler = partial(PreviewHandler, directory=directory, exports=exports)
    server = ThreadingHTTPServer(('127.0.0.1', port), handler)
    server.daemon_threads = True
    return server


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8779)
    parser.add_argument('--directory', type=Path, default=DEMO_ROOT)
    args = parser.parse_args()
    try:
        with make_server(args.port, args.directory) as server:
            print(f'Motion Diagram Studio preview: http://127.0.0.1:{server.server_port}/index.html', flush=True)
            server.serve_forever()
    except KeyboardInterrupt:
        return 0
    except (ValueError, OSError) as error:
        parser.exit(1, f'无法启动预览：{error}\n')


if __name__ == '__main__':
    raise SystemExit(main())
