"""Validate local export requests and HTTP queue behavior without rendering.

python -m unittest discover -s tests -p test_demo_exports.py -v
"""
import copy
import http.client
import json
import shutil
import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import export_demo as ed
import preview_server as ps


def actors(elements):
    for element in elements:
        if not isinstance(element, dict):
            continue
        if element.get('type') == 'drone':
            yield element
        nested = element.get('elements', element.get('children', []))
        if isinstance(nested, list):
            yield from actors(nested)


class RequestValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((ed.DEMO_ROOT / 'manifest.json').read_text(encoding='utf-8'))

    def test_all_39_blocks_both_themes_and_avatars(self):
        self.assertEqual(sum(len(d['exportViews']) for d in self.manifest), 39)
        for demo in self.manifest:
            for view in demo['exportViews']:
                for theme in ed.THEMES:
                    for avatar in ed.AVATARS:
                        with self.subTest(scene=demo['id'], view=view['id'], theme=theme, avatar=avatar):
                            payload = dict(scene=demo['id'], theme=theme, avatar=avatar, view=view['id'])
                            spec = ed.validate_request(payload)
                            self.assertEqual(spec.crop, tuple(view['crop']))
                            self.assertEqual((spec.width, spec.height), tuple(view['crop'][2:]))
                            self.assertEqual(spec.config['theme']['preset'], theme)
                            self.assertEqual(spec.config['canvas']['fps'], 30)
                            self.assertEqual(spec.config['canvas']['duration'], 12)
                            self.assertTrue(all(a['avatar'] == avatar for a in actors(spec.config['elements'])))
                            self.assertEqual(spec.filename, f"{demo['id']}-{theme}-{avatar}-{view['id']}.mp4")
                            path = ed.DEMO_ROOT / demo['id'] / ('config-light.json' if theme == ed.THEMES[1] else 'config-dark.json')
                            unchanged = json.loads(path.read_text(encoding='utf-8'))
                            self.assertTrue(all(a['avatar'] == 'spider' for a in actors(unchanged['elements'])))

    def test_full_view_and_reject_untrusted_fields_values_and_paths(self):
        self.assertIsNone(ed.validate_request({'scene': 'rag-explainer'}).crop)
        invalid = [None, [], 'scene', {}, {'scene': '../rag-explainer'},
                   {'scene': 'rag-explainer/../agent-team'}, {'scene': 'C:\\temp'},
                   {'scene': '%2e%2e'}, {'scene': 'unlisted-scene'},
                   {'scene': 'rag-explainer', 'theme': '../config'},
                   {'scene': 'rag-explainer', 'theme': None},
                   {'scene': 'rag-explainer', 'avatar': 'shell'},
                   {'scene': 'rag-explainer', 'view': '../rag-hero'},
                   {'scene': 'rag-explainer', 'view': 'rag-hero;whoami'},
                   {'scene': 'rag-explainer', 'view': 'not-allowed'},
                   {'scene': 'rag-explainer', 'crop': [0, 0, 2, 2]},
                   {'scene': 'rag-explainer', 'out': '../stolen.mp4'},
                   {'scene': 'rag-explainer', 'config': '/etc/passwd'}]
        for payload in invalid:
            with self.subTest(payload=payload), self.assertRaises(ValueError):
                ed.validate_request(payload)

    def test_invalid_trusted_crop_is_rejected(self):
        bad = [[-1, 0, 100, 100], [0, -1, 100, 100], [0, 0, 0, 100],
               [0, 0, 101, 100], [0, 0, 100, 101], [980, 0, 100, 100],
               [0, 1270, 100, 100], [False, 0, 100, 100], [0, 0, 100.0, 100],
               [0, 0, '100:100;injection', 100], [0, 0, 100], None]
        with tempfile.TemporaryDirectory(prefix='lp-crop-validation-') as temp:
            root = Path(temp)
            scene = root / 'rag-explainer'
            scene.mkdir()
            shutil.copyfile(ed.DEMO_ROOT / 'rag-explainer/config-dark.json', scene / 'config-dark.json')
            for area in bad:
                manifest = [{'id': 'rag-explainer', 'exportViews': [{'id': 'rag-hero', 'crop': area}]}]
                (root / 'manifest.json').write_text(json.dumps(manifest), encoding='utf-8')
                with self.subTest(crop=area), self.assertRaises(ValueError):
                    ed.validate_request({'scene': 'rag-explainer', 'view': 'rag-hero'}, root)


class ExportApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory(prefix='lp-api-test-')
        cls.root = Path(cls.tmp.name)
        manifest = json.loads((ed.DEMO_ROOT / 'manifest.json').read_text(encoding='utf-8'))
        (cls.root / 'manifest.json').write_text(json.dumps(manifest), encoding='utf-8')
        (cls.root / 'index.html').write_text('<!doctype html><title>Test gallery</title>', encoding='utf-8')
        for demo in manifest:
            folder = cls.root / demo['id']
            folder.mkdir()
            for name in ('config.json', 'config-dark.json', 'config-light.json'):
                shutil.copyfile(ed.DEMO_ROOT / demo['id'] / name, folder / name)
        cls.bytes = b'fake-video-bytes-for-http-only'
        cls.fail_next = threading.Event()
        cls.fail_next.clear()
        cls.worker_threads = set()
        def mock_export(spec, output, progress):
            cls.worker_threads.add(threading.get_ident())
            if cls.fail_next.is_set():
                cls.fail_next.clear()
                raise ed.ExportError('synthetic test failure')
            progress(50, 'test rendering')
            output.parent.mkdir(exist_ok=True)
            output.write_bytes(cls.bytes)
            return {'width': spec.width, 'height': spec.height, 'fps': 30,
                    'duration': 12, 'frames': 360, 'bytes': len(cls.bytes)}
        cls.export_patch = patch.object(ps, 'export', side_effect=mock_export)
        cls.export_patch.start()
        cls.server = ps.make_server(0, cls.root)
        cls.exports = cls.server.RequestHandlerClass.keywords['exports']
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.exports.pending.join()
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=5)
        cls.export_patch.stop()
        cls.tmp.cleanup()

    def request(self, method, path, body=None, headers=None):
        port = self.server.server_port
        request_headers = {'Host': f'127.0.0.1:{port}',
                           'Origin': f'http://127.0.0.1:{port}', 'Sec-Fetch-Site': 'same-origin'}
        if body is not None:
            request_headers['Content-Type'] = 'application/json'
            if not isinstance(body, (str, bytes)):
                body = json.dumps(body).encode('utf-8')
        request_headers.update(headers or {})
        conn = http.client.HTTPConnection('127.0.0.1', port, timeout=5)
        try:
            conn.request(method, path, body=body, headers=request_headers)
            response = conn.getresponse()
            return response.status, dict(response.getheaders()), response.read()
        finally:
            conn.close()

    def complete(self, job):
        deadline = time.monotonic() + 5
        while time.monotonic() < deadline:
            status, _, raw = self.request('GET', '/api/exports/' + job['id'])
            self.assertEqual(status, 200)
            current = json.loads(raw)
            if current['status'] in ('complete', 'failed'):
                return current
            time.sleep(.02)
        self.fail('mock export did not finish within five seconds')

    def test_post_status_download_and_filename(self):
        payload = {'scene': 'rag-explainer', 'theme': 'light-pastel', 'avatar': 'drone', 'view': 'rag-hero'}
        code, _, raw = self.request('POST', '/api/exports', payload)
        self.assertEqual(code, 202)
        job = self.complete(json.loads(raw))
        self.assertEqual(job['status'], 'complete')
        self.assertEqual(job['progress'], 100)
        self.assertEqual(job['filename'], 'rag-explainer-light-pastel-drone-rag-hero.mp4')
        self.assertEqual(job['url'], '/exports/' + job['id'] + '.mp4')
        code, headers, content = self.request('GET', job['url'])
        self.assertEqual(code, 200)
        self.assertEqual(content, self.bytes)
        self.assertEqual(headers['Content-Disposition'], 'attachment; filename="' + job['filename'] + '"')
        self.assertEqual(len(self.worker_threads), 1)

    def test_cross_site_invalid_host_and_body_limit_rejected(self):
        payload = {'scene': 'rag-explainer'}
        for headers in ({'Origin': 'https://attacker.example'},
                        {'Sec-Fetch-Site': 'cross-site'},
                        {'Host': 'attacker.example'},
                        {'Origin': f'http://127.0.0.1:{self.server.server_port}/path'}):
            with self.subTest(headers=headers):
                self.assertEqual(self.request('POST', '/api/exports', payload, headers)[0], 403)
        self.assertEqual(self.request('POST', '/api/exports', b' ' * (ps.BODY_LIMIT+1))[0], 413)
        self.assertEqual(self.request('POST', '/api/exports', b'{bad-json')[0], 400)
        self.assertEqual(self.request('POST', '/api/exports', [1, 2])[0], 400)
        self.assertEqual(self.request('POST', '/api/exports', payload, {'Content-Type': 'text/plain'})[0], 400)
        self.assertEqual(self.request('POST', '/api/exports', payload, {'Transfer-Encoding': 'chunked'})[0], 400)

    def test_failed_job_does_not_stop_single_worker(self):
        self.fail_next.set()
        with self.assertLogs(level='ERROR'):
            code, _, raw = self.request('POST', '/api/exports', {'scene': 'rag-explainer'})
            self.assertEqual(code, 202)
            failed = self.complete(json.loads(raw))
        self.assertEqual(failed['status'], 'failed')
        self.assertNotIn('url', failed)
        self.assertEqual(self.request('GET', '/exports/' + failed['id'] + '.mp4')[0], 404)
        code, _, raw = self.request('POST', '/api/exports', {'scene': 'rag-explainer'})
        self.assertEqual(code, 202)
        self.assertEqual(self.complete(json.loads(raw))['status'], 'complete')
        self.assertEqual(len(self.worker_threads), 1)

    def test_unlisted_and_encoded_export_paths_cannot_bypass_status(self):
        identity = '00000000-0000-0000-0000-000000000000'
        exports = self.root / 'exports'
        exports.mkdir(exist_ok=True)
        (exports / (identity+'.mp4')).write_bytes(self.bytes)
        for path in ('/exports/'+identity+'.mp4', '/%65xports/'+identity+'.mp4',
                     '/exports%2f'+identity+'.mp4', '/exports/../manifest.json',
                     '/.hidden', '/%2ehidden', '/api/exports/'+identity):
            with self.subTest(path=path):
                self.assertEqual(self.request('GET', path)[0], 404)


if __name__ == '__main__':
    unittest.main()
