#!/usr/bin/env python3
"""Build the short README GIF previews from existing public MP4 files.

python scripts/make_readme_previews.py
python scripts/make_readme_previews.py --compact

Only the Python standard library, FFmpeg and ffprobe are required. Every preview
is a six-second excerpt; the original videos are read without modification.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / 'assets' / 'readme'
REPORT = ROOT / 'out' / 'readme-preview-verification.json'
SCENES = ('rag-explainer', 'agent-team', 'product-request', 'knowledge-card',
          'business-workflow', 'incident-replay', 'component-lab', 'avatar-themes')
SECONDS, COLORS, WORKERS = 6, 128, 2
MAX_SINGLE_BYTES, MAX_TOTAL_BYTES = 2_000_000, 10_000_000


def sources(compact=False):
    width = 384 if compact else 432
    jobs = [{'source': ROOT / 'examples' / 'capability-demos' / scene / 'demo.mp4',
             'name': scene + '-dark.gif', 'width': width} for scene in SCENES]
    jobs += [
        {'source': ROOT / 'examples/capability-demos/rag-explainer/demo-light.mp4',
         'name': 'rag-explainer-light.gif', 'width': width},
        {'source': ROOT / 'examples/capability-demos/rag-explainer/demo-terminal.mp4',
         'name': 'rag-explainer-terminal.gif', 'width': width},
        {'source': ROOT / 'examples/capability-demos/rag-explainer/demo-pastel.mp4',
         'name': 'rag-explainer-pastel.gif', 'width': width},
        {'source': ROOT / 'media/recreations/first-recreation.mp4',
         'name': 'first-recreation.gif', 'width': width},
        {'source': ROOT / 'media/recreations/spider-recreation.mp4',
         'name': 'spider-recreation.gif', 'width': width},
        {'source': ROOT / 'media/exports/robot/rag-rerank-light-drone.mp4',
         'name': 'rag-rerank-light-drone.gif', 'width': 384 if compact else 478},
    ]
    for job in jobs:
        job['source'] = job['source'].resolve()
        if not job['source'].is_relative_to(ROOT.resolve()):
            raise ValueError('输入视频超出项目目录。')
    return jobs


def _run(command, timeout=600):
    try:
        result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8',
                                errors='replace', timeout=timeout)
    except subprocess.TimeoutExpired as error:
        raise RuntimeError('生成或检查 GIF 超时。') from error
    if result.returncode:
        raise RuntimeError(result.stderr[-3000:].strip() or 'FFmpeg 处理失败。')
    return result.stdout


def _sha256(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def _probe(path, ffprobe, count_frames=True):
    command = [ffprobe, '-v', 'error']
    if count_frames:
        command.append('-count_frames')
    command += ['-select_streams', 'v:0', '-show_entries',
                'stream=codec_name,width,height,duration,nb_read_frames,avg_frame_rate:format=duration',
                '-of', 'json', str(path)]
    return json.loads(_run(command))


def _preview(job, fps, ffmpeg, ffprobe):
    source = job['source']
    before = _sha256(source)
    output = (OUTPUT / job['name']).resolve()
    if output.parent != OUTPUT.resolve():
        raise ValueError('GIF 输出目录无效。')
    pending = output.with_name(output.stem + '.pending.gif')
    width = job['width']
    filters = (f'[0:v]fps={fps},scale={width}:-1:flags=lanczos,split[frames][stats];'
               f'[stats]palettegen=max_colors={COLORS}[palette];'
               '[frames][palette]paletteuse=dither=sierra2_4a:diff_mode=rectangle')
    try:
        _run([ffmpeg, '-y', '-v', 'error', '-threads', '2', '-t', str(SECONDS), '-i', str(source),
              '-filter_complex_threads', '1', '-filter_complex', filters,
              '-an', '-loop', '0', str(pending)])
        source_info = _probe(source, ffprobe, count_frames=False)['streams'][0]
        info = _probe(pending, ffprobe)
        video = info['streams'][0]
        frames = int(video.get('nb_read_frames', 0))
        duration = float(video.get('duration') or info.get('format', {}).get('duration') or 0)
        expected_height = round(source_info['height'] * width / source_info['width'])
        if video.get('codec_name') != 'gif' or video['width'] != width or video['height'] != expected_height:
            raise RuntimeError('GIF 尺寸或编码与指定参数不一致。')
        if frames != SECONDS * fps or abs(duration - SECONDS) > .03:
            raise RuntimeError('GIF 的帧数或时长不完整。')
        hashes = _run([ffmpeg, '-v', 'error', '-xerror', '-ignore_loop', '1', '-i', str(pending),
                       '-map', '0:v:0', '-f', 'framemd5', '-'])
        decoded = [line for line in hashes.splitlines() if line and not line.startswith('#')]
        distinct = {line.rsplit(',', 1)[-1].strip() for line in decoded}
        if len(decoded) != frames or len(distinct) < 2:
            raise RuntimeError('GIF 未包含可完整解码的变化画面。')
        after = _sha256(source)
        if after != before:
            raise RuntimeError('原始 MP4 在处理期间发生变化。')
        os.replace(pending, output)
        return {'file': output.relative_to(ROOT).as_posix(),
                'source': source.relative_to(ROOT).as_posix(),
                'sourceSha256': before, 'sourceUnchanged': True,
                'width': video['width'], 'height': video['height'],
                'duration': duration, 'frames': frames, 'previewFps': fps,
                'distinctDecodedFrames': len(distinct), 'fullDecode': 'passed',
                'bytes': output.stat().st_size, 'loop': 0, 'maxColors': COLORS,
                'dither': 'sierra2_4a', 'diffMode': 'rectangle', 'passed': True}
    finally:
        pending.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--compact', action='store_true', help='use width 384 and 6 fps to reduce the GIF total size')
    args = parser.parse_args()
    ffmpeg, ffprobe = shutil.which('ffmpeg'), shutil.which('ffprobe')
    if not ffmpeg or not ffprobe:
        parser.exit(1, '未找到 ffmpeg 或 ffprobe，请安装 FFmpeg 并加入 PATH。\n')
    jobs = sources(args.compact)
    missing = [job['source'].relative_to(ROOT).as_posix() for job in jobs if not job['source'].is_file()]
    if missing:
        parser.exit(1, '缺少以下视频，请先生成或恢复对应 MP4：\n' + '\n'.join(missing) + '\n')
    OUTPUT.mkdir(parents=True, exist_ok=True)
    fps = 6 if args.compact else 8
    records, errors = [], []
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        pending = {pool.submit(_preview, job, fps, ffmpeg, ffprobe): job for job in jobs}
        for future in as_completed(pending):
            job = pending[future]
            try:
                record = future.result()
                records.append(record)
                print(f"READY {job['name']} | {record['width']}x{record['height']} | "
                      f"{record['frames']} frames | {record['bytes']} B", flush=True)
            except Exception as error:
                errors.append({'file': job['name'], 'error': str(error)})
                print(f"FAILED {job['name']}: {error}", flush=True)
    ordering = {job['name']: i for i, job in enumerate(jobs)}
    records.sort(key=lambda r: ordering[Path(r['file']).name])
    total = sum(record['bytes'] for record in records)
    budget = total < MAX_TOTAL_BYTES and all(record['bytes'] < MAX_SINGLE_BYTES for record in records)
    passed = len(records) == len(jobs) and not errors and budget
    report = {'passed': passed, 'createdAt': datetime.now(timezone.utc).isoformat(),
              'previewCount': len(records), 'excerptSeconds': SECONDS, 'previewFps': fps,
              'workers': WORKERS, 'totalBytes': total, 'maxSingleBytes': MAX_SINGLE_BYTES,
              'maxTotalBytes': MAX_TOTAL_BYTES, 'sizeBudgetPassed': budget,
              'scope': f'{len(jobs)} 个 GIF 均为已有 MP4 的前 6 秒节选，完整视频通过 README 链接查看。',
              'files': records, 'errors': errors}
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    with REPORT.open('w', encoding='utf-8', newline='\n') as stream:
        stream.write(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(f"{'PASS' if passed else 'FAIL'}: {len(records)}/{len(jobs)} GIFs, total {total} B", flush=True)
    if not budget and not args.compact:
        print('GIF 超过体积目标，可运行 --compact 降至宽 384 / 6 fps。', flush=True)
    return 0 if passed else 1


if __name__ == '__main__':
    raise SystemExit(main())
