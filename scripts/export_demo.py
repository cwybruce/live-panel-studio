#!/usr/bin/env python3
"""Export a whitelisted demo or its named block using the existing renderer.

python scripts/export_demo.py --scene rag-explainer --theme light-pastel \
    --avatar drone --view rag-hero --out my-rag.mp4
"""
from __future__ import annotations

import argparse
import copy
from dataclasses import dataclass
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import tempfile
import threading
from typing import Callable

import livepanel as lp

DEMO_ROOT = Path(__file__).resolve().parent.parent / 'examples' / 'capability-demos'
THEME_CONFIGS = {'terminal-dark': 'config-dark.json', 'light-pastel': 'config-light.json',
                 'terminal-classic': 'config-terminal.json', 'pastel-classic': 'config-pastel.json'}
THEME_PRESETS = {'terminal-dark': 'terminal-dark', 'light-pastel': 'light-pastel',
                 'terminal-classic': 'terminal-dark', 'pastel-classic': 'light-pastel'}
STYLE_CONFIGS = {'diagram': THEME_CONFIGS,
                 'terminal': {'terminal-dark': 'config-console-dark.json',
                              'light-pastel': 'config-console-light.json',
                              'terminal-classic': 'config-console-terminal.json',
                              'pastel-classic': 'config-console-pastel.json'}}
STYLES = tuple(STYLE_CONFIGS)
THEMES = tuple(THEME_CONFIGS)
AVATARS = ('spider', 'drone')
IDENTIFIER = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
VIEW_IDENTIFIER = re.compile(r'^[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*$')
FPS, DURATION = 30, 12


class ExportError(RuntimeError):
    """An export could not be rendered or verified."""


@dataclass(frozen=True)
class ExportSpec:
    scene: str
    theme: str
    avatar: str
    view: str
    config: dict
    source_width: int
    source_height: int
    crop: tuple[int, int, int, int] | None
    filename: str
    style: str = 'diagram'

    @property
    def width(self):
        return self.crop[2] if self.crop else self.source_width

    @property
    def height(self):
        return self.crop[3] if self.crop else self.source_height


def _inside(root: Path, child: Path) -> Path:
    child = child.resolve()
    if not child.is_relative_to(root.resolve()):
        raise ValueError('示例路径超出允许目录。')
    return child


def _avatar_elements(elements, avatar):
    for element in elements:
        if not isinstance(element, dict):
            continue
        if element.get('type') == 'drone':
            element['avatar'] = avatar
        children = element.get('elements', element.get('children', []))
        if isinstance(children, list):
            _avatar_elements(children, avatar)


def validate_request(payload: dict, demo_root: Path = DEMO_ROOT) -> ExportSpec:
    """Resolve all source paths and crops from trusted local metadata only."""
    if not isinstance(payload, dict):
        raise ValueError('请求必须是 JSON 对象。')
    if set(payload) - {'scene', 'theme', 'avatar', 'view', 'style'}:
        raise ValueError('请求包含不支持的字段。')
    scene = payload.get('scene')
    theme = payload.get('theme', THEMES[0])
    avatar = payload.get('avatar', AVATARS[0])
    view = payload.get('view', 'full')
    style = payload.get('style', STYLES[0])
    if not isinstance(scene, str) or not IDENTIFIER.fullmatch(scene):
        raise ValueError('请选择有效的示例。')
    if not isinstance(theme, str) or theme not in THEMES:
        raise ValueError('请选择支持的主题。')
    if not isinstance(style, str) or style not in STYLES:
        raise ValueError('请选择支持的展示样式。')
    if not isinstance(avatar, str) or avatar not in AVATARS:
        raise ValueError('请选择支持的角色。')
    if not isinstance(view, str) or not VIEW_IDENTIFIER.fullmatch(view):
        raise ValueError('请选择有效的导出视图。')
    root = demo_root.resolve()
    with (root / 'manifest.json').open(encoding='utf-8') as f:
        manifest = json.load(f)
    match = next((d for d in manifest if d.get('id') == scene), None)
    if match is None:
        raise ValueError('这个示例不在导出列表中。')
    scene_dir = _inside(root, root / scene)
    filename = STYLE_CONFIGS[style][theme]
    if style != STYLES[0]:
        styles = match.get('styleVariants', {})
        style_record = styles.get(style, {}) if isinstance(styles, dict) else {}
        variants = style_record.get('themeVariants', {}) if isinstance(style_record, dict) else {}
        variant = variants.get(theme, {}) if isinstance(variants, dict) else {}
        if not isinstance(variant, dict) or variant.get('config') != filename:
            raise ValueError('这个示例的展示样式不在导出列表中。')
    config_path = _inside(root, scene_dir / filename)
    if not config_path.is_file() and style == STYLES[0] and theme == THEMES[0]:
        config_path = _inside(root, scene_dir / 'config.json')
    if not config_path.is_file():
        raise ValueError('这个示例的主题配置尚未准备好。')
    with config_path.open(encoding='utf-8') as f:
        config = copy.deepcopy(json.load(f))
    presentation = config.get('presentation', {})
    if not isinstance(presentation, dict) or presentation.get('style', STYLES[0]) != style:
        raise ValueError('配置中的展示样式与所选方案不一致，请重新生成示例。')
    selected = config.get('theme', {})
    if (selected.get('preset') != THEME_PRESETS[theme]
            or selected.get('variant', selected.get('preset')) != theme):
        raise ValueError('主题配置与所选方案不一致，请重新生成示例。')
    width, height, _, _ = lp.canvas(config)
    if type(width) is not int or type(height) is not int or min(width, height) <= 0 or width % 2 or height % 2:
        raise ValueError('示例画布尺寸无效。')
    crop = None
    if view != 'full':
        block = next((b for b in match.get('exportViews', []) if b.get('id') == view), None)
        if block is None:
            raise ValueError('这个视图不在允许导出的列表中。')
        area = block.get('crop')
        if not isinstance(area, list) or len(area) != 4 or any(type(n) is not int for n in area):
            raise ValueError('视图裁剪配置无效。')
        x, y, w, h = area
        if min(x, y) < 0 or min(w, h) <= 0 or w % 2 or h % 2 or x + w > width or y + h > height:
            raise ValueError('视图裁剪范围超出画布，或尺寸不是偶数。')
        crop = tuple(area)
    config.setdefault('canvas', {}).update(width=width, height=height, duration=DURATION, fps=FPS)
    _avatar_elements(config.get('elements', []), avatar)
    style_suffix = '' if style == STYLES[0] else f'-{style}'
    return ExportSpec(scene, theme, avatar, view, config, width, height, crop,
                      f'{scene}{style_suffix}-{theme}-{avatar}-{view}.mp4', style=style)


def _executable(names, what):
    try:
        return lp.find_exe(None, names, what)
    except SystemExit as e:
        raise ExportError(str(e)) from e


def _run(command, timeout=600):
    try:
        done = subprocess.run(command, capture_output=True, text=True,
                              encoding='utf-8', errors='replace', timeout=timeout)
    except subprocess.TimeoutExpired as e:
        raise ExportError('视频处理超时，请稍后重试。') from e
    if done.returncode:
        raise ExportError((done.stderr or done.stdout or '视频处理失败。')[-3000:].strip())
    return done.stdout


def verify_video(path: Path, width: int, height: int, ffmpeg=None, ffprobe=None):
    """Check dimensions, timing, frame count, and decode every video frame."""
    ffmpeg = ffmpeg or _executable(['ffmpeg'], 'ffmpeg')
    ffprobe = ffprobe or _executable(['ffprobe'], 'ffprobe')
    raw = _run([ffprobe, '-v', 'error', '-count_frames', '-select_streams', 'v:0',
                '-show_entries', 'stream=width,height,r_frame_rate,nb_read_frames,duration:format=duration',
                '-of', 'json', str(path)])
    probe = json.loads(raw)
    streams = probe.get('streams', [])
    if not streams:
        raise ExportError('导出文件缺少视频画面。')
    stream = streams[0]
    numerator, denominator = map(int, stream['r_frame_rate'].split('/'))
    rate = numerator / denominator if denominator else 0
    duration = float(stream.get('duration') or probe.get('format', {}).get('duration') or 0)
    if (stream.get('width'), stream.get('height')) != (width, height):
        raise ExportError('导出尺寸与所选视图不一致。')
    if abs(rate - FPS) > .01 or abs(duration - DURATION) > 1 / FPS + .01:
        raise ExportError('导出帧率或时长不符合要求。')
    if int(stream.get('nb_read_frames', 0)) != FPS * DURATION:
        raise ExportError('视频帧数不完整。')
    _run([ffmpeg, '-v', 'error', '-xerror', '-i', str(path), '-map', '0:v:0',
          '-f', 'null', os.devnull])
    return {'width': width, 'height': height, 'fps': FPS, 'duration': DURATION,
            'frames': FPS * DURATION, 'bytes': path.stat().st_size}


def _render(spec, config_path, output, progress, ffmpeg):
    command = [sys.executable, str(Path(__file__).with_name('render.py')), '--config', str(config_path),
               '--out', str(output), '--width', str(spec.source_width), '--height', str(spec.source_height),
               '--fps', str(FPS), '--duration', str(DURATION), '--ffmpeg', ffmpeg,
               '--html-out', str(output.parent / 'page.html')]
    environment = dict(os.environ, PYTHONUTF8='1')
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                               text=True, encoding='utf-8', errors='replace', env=environment,
                               start_new_session=os.name != 'nt')
    expired = threading.Event()
    stop_lock = threading.Lock()
    def stop_tree():
        with stop_lock:
            if process.poll() is not None:
                return
            if os.name == 'nt':
                try:
                    subprocess.run(['taskkill', '/PID', str(process.pid), '/T', '/F'],
                                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=15)
                except (OSError, subprocess.TimeoutExpired):
                    if process.poll() is None:
                        process.kill()
            else:
                try:
                    os.killpg(process.pid, signal.SIGTERM)
                    process.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
            if process.poll() is None:
                process.kill()
    def timeout():
        expired.set()
        stop_tree()
    timer = threading.Timer(600, timeout)
    timer.daemon = True
    timer.start()
    tail = []
    try:
        for item in process.stdout:
            tail.append(item)
            tail = tail[-30:]
            hit = re.search(r'(\d+)/(\d+) frames', item)
            if hit:
                current, total = map(int, hit.groups())
                progress(5 + 80 * current / max(1, total), '正在渲染动画')
        result = process.wait()
        if expired.is_set():
            raise ExportError('动画渲染超时，请稍后重试。')
        if result:
            raise ExportError(''.join(tail)[-3000:].strip() or '动画渲染失败。')
    finally:
        timer.cancel()
        stop_tree()
        process.wait()
        process.stdout.close()


def export(spec: ExportSpec, output: Path, progress: Callable[[float, str], None] | None = None):
    """Render in a temporary folder, then publish only a fully verified result."""
    progress = progress or (lambda value, stage: None)
    output = output.resolve()
    if output.suffix.lower() != '.mp4':
        raise ValueError('输出文件必须使用 .mp4 扩展名。')
    output.parent.mkdir(parents=True, exist_ok=True)
    ffmpeg = _executable(['ffmpeg'], 'ffmpeg')
    ffprobe = _executable(['ffprobe'], 'ffprobe')
    _executable(lp.CHROME_NAMES, 'Chrome')
    progress(2, '正在准备所选主题与角色')
    with tempfile.TemporaryDirectory(prefix='.live-panel-export-', dir=output.parent) as folder:
        work = Path(folder).resolve()
        if not work.is_relative_to(output.parent):
            raise ExportError('临时导出目录不在目标目录内。')
        config_path = work / 'config.json'
        config_path.write_text(json.dumps(spec.config, ensure_ascii=False), encoding='utf-8')
        full = work / 'full.mp4'
        _render(spec, config_path, full, progress, ffmpeg)
        ready = full
        if spec.crop:
            progress(87, '正在导出所选分区')
            x, y, w, h = spec.crop
            ready = work / 'view.pending.mp4'
            _run([ffmpeg, '-y', '-loglevel', 'error', '-i', str(full), '-vf',
                  f'crop={w}:{h}:{x}:{y}:exact=1', '-c:v', 'libx264', '-preset', 'medium',
                  '-crf', '16', '-pix_fmt', 'yuv420p', '-r', str(FPS), '-c:a', 'copy',
                  '-movflags', '+faststart', str(ready)])
        progress(94, '正在检查视频完整性')
        info = verify_video(ready, spec.width, spec.height, ffmpeg, ffprobe)
        os.replace(ready, output)
    progress(100, '导出完成')
    return info


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scene', required=True)
    parser.add_argument('--theme', choices=THEMES, default=THEMES[0])
    parser.add_argument('--style', choices=STYLES, default=STYLES[0])
    parser.add_argument('--avatar', choices=AVATARS, default=AVATARS[0])
    parser.add_argument('--view', default='full')
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    try:
        spec = validate_request({'scene': args.scene, 'theme': args.theme,
                                 'avatar': args.avatar, 'view': args.view, 'style': args.style})
        info = export(spec, Path(args.out), lambda value, stage: print(f'{value:.0f}% {stage}', flush=True))
        print(json.dumps({'file': str(Path(args.out).resolve()), **info}, ensure_ascii=False))
    except (ValueError, ExportError, OSError, json.JSONDecodeError) as e:
        print(f'导出失败：{e}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
