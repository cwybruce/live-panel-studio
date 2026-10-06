#!/usr/bin/env python3
"""Verify every named block by cropping the already rendered light demo videos.

python scripts/verify_demo_exports.py --run

No Chrome rendering is repeated. Inputs and output locations come only from the
local demo manifest; two FFmpeg tasks run at a time.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess

from export_demo import (DEMO_ROOT, DURATION, FPS, THEMES, ExportError,
                         _executable, validate_request, verify_video)

REPORT = DEMO_ROOT / 'export-verification.json'
BLOCK_ROOT = DEMO_ROOT / 'exports' / 'block-checks'
WORKERS = 2
EXPECTED_DEMOS, EXPECTED_BLOCKS = 8, 39


def _save(report):
    temporary = REPORT.with_name(REPORT.stem + '.pending.json')
    temporary.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    os.replace(temporary, REPORT)


def _relative(path):
    return Path(path).resolve().relative_to(DEMO_ROOT.resolve()).as_posix()


def _path(scene, filename):
    path = (DEMO_ROOT / scene / filename).resolve()
    if not path.is_relative_to(DEMO_ROOT.resolve()):
        raise ValueError('Manifest path leaves the demo directory')
    return path


def _source_check(job, ffmpeg, ffprobe):
    demo, theme, spec, video = job
    info = verify_video(video, spec.source_width, spec.source_height, ffmpeg, ffprobe)
    return {'scene': demo['id'], 'theme': theme, 'avatar': 'spider',
            'config': demo['id'] + ('/config-light.json' if theme == THEMES[1] else '/config-dark.json'),
            'configTheme': spec.config.get('theme', {}).get('preset'),
            'sourceVideo': _relative(video), 'passed': True, **info}


def _crop_check(job, ffmpeg, ffprobe):
    demo, view, spec, source = job
    output = (BLOCK_ROOT / spec.scene / (spec.view + '.mp4')).resolve()
    if not output.is_relative_to(BLOCK_ROOT.resolve()):
        raise ValueError('Block output leaves the fixed verification directory')
    output.parent.mkdir(parents=True, exist_ok=True)
    pending = output.with_name(output.stem + '.pending.mp4')
    x, y, w, h = spec.crop
    record = {'scene': spec.scene, 'view': spec.view, 'label': view.get('label', spec.view),
              'theme': 'light-pastel', 'avatar': 'spider',
              'config': spec.scene + '/config-light.json',
              'configTheme': spec.config.get('theme', {}).get('preset'),
              'sourceVideo': _relative(source), 'output': _relative(output),
              'crop': [x, y, w, h], 'method': 'crop pre-rendered full frames'}
    try:
        command = [ffmpeg, '-y', '-loglevel', 'error', '-threads', '2', '-i', str(source),
                   '-vf', f'crop={w}:{h}:{x}:{y}:exact=1', '-c:v', 'libx264', '-threads', '2',
                   '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', '-r', str(FPS),
                   '-c:a', 'copy', '-movflags', '+faststart', str(pending)]
        result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8',
                                errors='replace', timeout=600)
        if result.returncode:
            raise ExportError(result.stderr[-3000:].strip() or 'FFmpeg crop failed')
        info = verify_video(pending, w, h, ffmpeg, ffprobe)
        os.replace(pending, output)
        return {**record, 'passed': True, **info}
    except Exception as error:
        pending.unlink(missing_ok=True)
        return {**record, 'passed': False, 'error': str(error)}


def _sample():
    metadata = DEMO_ROOT / 'exports' / 'check-rag-light-drone-hero.json'
    if not metadata.is_file():
        return None
    record = json.loads(metadata.read_text(encoding='utf-8'))
    record['evidenceFile'] = _relative(metadata)
    if record.get('file'):
        record['file'] = _relative(Path(record['file']))
    record['method'] = 'independent Chrome renderer with selected theme and avatar, followed by crop'
    return record


def run():
    report = {'passed': False, 'status': 'running',
              'startedAt': datetime.now(timezone.utc).isoformat(),
              'fps': FPS, 'duration': DURATION, 'framesPerVideo': FPS * DURATION,
              'workers': WORKERS,
              'scope': '从已生成的浅色默认蜘蛛完整视频，裁剪 manifest 中全部 39 个命名分区；验证尺寸、帧率、时长、360 帧与完整解码。',
              'evidenceBounds': '分区矩阵使用既有完整画面验证裁剪和编码。独立 Chrome 与角色选择导出的样例记录见 realRendererSample。',
              'fullSources': [], 'blocks': []}
    _save(report)
    try:
        manifest = json.loads((DEMO_ROOT / 'manifest.json').read_text(encoding='utf-8'))
        if len(manifest) != EXPECTED_DEMOS:
            raise ValueError(f'Expected {EXPECTED_DEMOS} demos; found {len(manifest)}')
        block_count = sum(len(d.get('exportViews', [])) for d in manifest)
        if block_count != EXPECTED_BLOCKS:
            raise ValueError(f'Expected {EXPECTED_BLOCKS} named blocks; found {block_count}')
        source_jobs, block_jobs, unfinished = [], [], []
        for demo in manifest:
            for theme in THEMES:
                spec = validate_request({'scene': demo['id'], 'theme': theme,
                                         'avatar': 'spider', 'view': 'full'})
                filename = 'demo-light.mp4' if theme == THEMES[1] else 'demo.mp4'
                video = _path(demo['id'], filename)
                pending = video.with_name(video.stem + '.pending.mp4')
                if not video.is_file() or not video.stat().st_size or pending.exists():
                    unfinished.append(_relative(video))
                source_jobs.append((demo, theme, spec, video))
            for view in demo['exportViews']:
                spec = validate_request({'scene': demo['id'], 'theme': 'light-pastel',
                                         'avatar': 'spider', 'view': view['id']})
                block_jobs.append((demo, view, spec, _path(demo['id'], 'demo-light.mp4')))
        if unfinished:
            raise ValueError('Wait for all 16 full videos to finish rendering: ' + ', '.join(unfinished))
        ffmpeg = _executable(['ffmpeg'], 'ffmpeg')
        ffprobe = _executable(['ffprobe'], 'ffprobe')
        with ThreadPoolExecutor(max_workers=WORKERS) as pool:
            futures = {pool.submit(_source_check, job, ffmpeg, ffprobe): job for job in source_jobs}
            for future in as_completed(futures):
                info = future.result()
                report['fullSources'].append(info)
                print(f"SOURCE {len(report['fullSources'])}/16 {info['scene']} {info['theme']} PASS", flush=True)
        with ThreadPoolExecutor(max_workers=WORKERS) as pool:
            futures = {pool.submit(_crop_check, job, ffmpeg, ffprobe): job for job in block_jobs}
            for future in as_completed(futures):
                info = future.result()
                report['blocks'].append(info)
                print(f"BLOCK {len(report['blocks'])}/{EXPECTED_BLOCKS} {info['scene']} {info['view']} "
                      + ('PASS' if info['passed'] else 'FAIL'), flush=True)
        order = {demo['id']: i for i, demo in enumerate(manifest)}
        report['fullSources'].sort(key=lambda s: (order[s['scene']], s['theme']))
        report['blocks'].sort(key=lambda b: (order[b['scene']], b['view']))
        report['realRendererSample'] = _sample()
        report['fullVideoCount'] = len(report['fullSources'])
        report['blockCount'] = len(report['blocks'])
        report['passed'] = (len(report['fullSources']) == 16 and len(report['blocks']) == EXPECTED_BLOCKS
                            and all(b['passed'] for b in report['blocks'])
                            and all(s['passed'] for s in report['fullSources']))
        report['status'] = 'complete' if report['passed'] else 'failed'
    except Exception as error:
        report['status'] = 'failed'
        report['error'] = str(error)
    report['finishedAt'] = datetime.now(timezone.utc).isoformat()
    _save(report)
    print(json.dumps({'passed': report['passed'], 'sources': len(report['fullSources']),
                      'blocks': len(report['blocks']), 'report': _relative(REPORT)}, ensure_ascii=False), flush=True)
    return 0 if report['passed'] else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', action='store_true', default=True, help='run the complete verification matrix (default)')
    parser.parse_args()
    return run()


if __name__ == '__main__':
    raise SystemExit(main())
