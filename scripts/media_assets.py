#!/usr/bin/env python3
"""Package and restore versioned demo media using only Python's standard library.

python scripts/media_assets.py pack
python scripts/media_assets.py pack --tag media-v2 --include examples/my-demo/demo.mp4
python scripts/media_assets.py download --set demos
python scripts/media_assets.py download --set all --dest out/site
python scripts/media_assets.py check --set all

MP4s keep their original relative paths. Existing files are reused only when
their hashes match; locally edited videos are never silently overwritten.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import tempfile
import time
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / 'media/assets-manifest.json'
REPOSITORY = 'cwybruce/motion-diagram-studio'
RELEASE_TAG = 'media-v1'
BUNDLE_NAME = 'motion-diagram-studio-media-v1.zip'
CHUNK = 1024 * 1024
MAX_BUNDLE_BYTES = 2 * 1024 ** 3 - 1
HASH = re.compile(r'^[0-9a-f]{64}$')
RESERVED = re.compile(r'^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\.|$)', re.I)


class MediaError(ValueError):
    """Invalid or incomplete media, or a destination that cannot be restored safely."""


def safe_path(value):
    """Accept portable POSIX relative file paths, including on Windows."""
    if not isinstance(value, str) or not value or value.startswith('/'):
        raise MediaError(f'Unsafe media path: {value!r}')
    if any(ord(c) < 32 or ord(c) == 127 or c in '\\<>:"|?*' for c in value):
        raise MediaError(f'Unsafe media path: {value!r}')
    parts = value.split('/')
    if any(p in ('', '.', '..') or p.endswith((' ', '.')) or RESERVED.match(p) for p in parts):
        raise MediaError(f'Unsafe media path: {value!r}')
    return value


def file_sha256(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as source:
        for chunk in iter(lambda: source.read(CHUNK), b''):
            digest.update(chunk)
    return digest.hexdigest()


def _unique_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise MediaError(f'duplicate JSON key: {key}')
        result[key] = value
    return result


def validate_manifest(data):
    if not isinstance(data, dict) or data.get('version') != 1:
        raise MediaError('Unsupported media manifest version.')
    if type(data.get('published')) is not bool:
        raise MediaError('The manifest must declare a boolean published status.')
    repo, tag = data.get('repository'), data.get('releaseTag')
    if not isinstance(repo, str) or not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', repo):
        raise MediaError('Invalid media repository.')
    if not isinstance(tag, str) or not re.fullmatch(r'[A-Za-z0-9_.-]+', tag) or tag in ('.', '..'):
        raise MediaError('Invalid media release tag.')
    published_tags = data.get('publishedTags', [])
    if (not isinstance(published_tags, list)
            or any(not isinstance(t, str) or not re.fullmatch(r'[A-Za-z0-9_.-]+', t) or t in ('.', '..')
                   for t in published_tags)
            or len(published_tags) != len(set(published_tags))):
        raise MediaError('Invalid published media tag history.')
    bundle = data.get('bundle')
    if not isinstance(bundle, dict):
        raise MediaError('Missing media bundle.')
    name = safe_path(bundle.get('filename'))
    if '/' in name or not name.endswith('.zip'):
        raise MediaError('The bundle must have a plain ZIP filename.')
    expected_url = f'https://github.com/{repo}/releases/download/{tag}/{name}'
    if bundle.get('url') != expected_url:
        raise MediaError('The bundle URL must identify the registered GitHub release asset.')
    if type(bundle.get('size')) is not int or not 0 < bundle['size'] <= MAX_BUNDLE_BYTES:
        raise MediaError('Invalid registered bundle size.')
    if not isinstance(bundle.get('sha256'), str) or not HASH.fullmatch(bundle['sha256']):
        raise MediaError('Invalid registered bundle SHA-256.')
    assets = data.get('assets')
    if not isinstance(assets, list) or not assets:
        raise MediaError('The bundle has no asset inventory.')
    seen = set()
    for asset in assets:
        if not isinstance(asset, dict):
            raise MediaError('Invalid media asset entry.')
        path = safe_path(asset.get('path'))
        folded = path.casefold()
        if folded in seen:
            raise MediaError(f'duplicate manifest path: {path}')
        seen.add(folded)
        if type(asset.get('size')) is not int or not 0 <= asset['size'] <= MAX_BUNDLE_BYTES:
            raise MediaError(f'Invalid registered asset size: {path}')
        if not isinstance(asset.get('sha256'), str) or not HASH.fullmatch(asset['sha256']):
            raise MediaError(f'Invalid registered asset SHA-256: {path}')
        if asset.get('set') not in ('demos', 'all'):
            raise MediaError(f'Invalid media set: {path}')
        if asset.get('type') == 'video':
            if not path.endswith('.mp4') or not path.startswith(('examples/', 'media/')):
                raise MediaError(f'Invalid video inventory path: {path}')
        elif asset.get('type') == 'metadata':
            prefix = f'media/release-notices/{tag}/'
            if not path.startswith(prefix) or path[len(prefix):] not in ('README.md', 'LICENSE', 'THIRD_PARTY_NOTICES.md'):
                raise MediaError(f'Invalid metadata inventory path: {path}')
        else:
            raise MediaError(f'Invalid asset type: {path}')
    if sum(asset['size'] for asset in assets) > MAX_BUNDLE_BYTES:
        raise MediaError('The registered unpacked media exceed the bundle size limit.')
    return data


def load_manifest(path=DEFAULT_MANIFEST):
    try:
        data = json.loads(Path(path).read_text(encoding='utf-8'), object_pairs_hook=_unique_keys)
    except (OSError, json.JSONDecodeError) as error:
        raise MediaError(f'Cannot read media manifest: {error}') from error
    return validate_manifest(data)


def published_paths(manifest_path=DEFAULT_MANIFEST):
    """Return registered public video paths, without requiring local media files."""
    path = Path(manifest_path)
    if not path.exists():
        return set()
    data = load_manifest(path)
    if not data['published']:
        return set()
    return {a['path'] for a in data['assets'] if a['type'] == 'video'}


def _selected(data, media_set):
    if media_set not in ('demos', 'all'):
        raise MediaError('Choose --set demos or --set all.')
    return [a for a in data['assets'] if a['type'] == 'metadata' or media_set == 'all' or a['set'] == 'demos']


def _target(dest, relative):
    """Check the destination and every existing ancestor before any filesystem write."""
    dest = Path(dest).absolute()
    target = dest.joinpath(*safe_path(relative).split('/'))
    for ancestor in list(reversed(dest.parents)) + [dest]:
        if _link_like(ancestor):
            raise MediaError(f'Refusing symlink destination: {ancestor}')
    current = dest
    for part in safe_path(relative).split('/'):
        current = current / part
        if _link_like(current):
            raise MediaError(f'Refusing symlink destination: {current}')
    if not target.resolve().is_relative_to(dest.resolve()):
        raise MediaError(f'Media destination resolves outside its directory: {relative}')
    return target


def _link_like(path):
    if path.is_symlink():
        return True
    try:
        tag = getattr(path.lstat(), 'st_reparse_tag', None)
        return tag is not None and tag in (getattr(stat, 'IO_REPARSE_TAG_MOUNT_POINT', 0xA0000003),
                                          getattr(stat, 'IO_REPARSE_TAG_SYMLINK', 0xA000000C))
    except FileNotFoundError:
        return False


def _matches(path, asset):
    return path.is_file() and path.stat().st_size == asset['size'] and file_sha256(path) == asset['sha256']


def check(manifest_path=DEFAULT_MANIFEST, dest=ROOT, media_set='all'):
    data = load_manifest(manifest_path)
    result = {'set': media_set, 'verified': [], 'missing': [], 'modified': []}
    for asset in _selected(data, media_set):
        path = _target(dest, asset['path'])
        if not path.exists():
            result['missing'].append(asset['path'])
        elif _matches(path, asset):
            result['verified'].append(asset['path'])
        else:
            result['modified'].append(asset['path'])
    result['passed'] = not result['missing'] and not result['modified']
    return result


def _fetch(bundle, output):
    request = urllib.request.Request(bundle['url'], headers={'User-Agent': 'MotionDiagramStudio-media/1'})
    digest, total = hashlib.sha256(), 0
    deadline = time.monotonic() + 600
    with urllib.request.urlopen(request, timeout=30) as response, Path(output).open('wb') as target:
        length = response.headers.get('Content-Length')
        if length is not None and (not length.isdigit() or int(length) != bundle['size']):
            raise MediaError('Downloaded bundle Content-Length differs from registered size.')
        while True:
            if time.monotonic() >= deadline:
                raise MediaError('Media bundle download exceeded its total timeout.')
            chunk = response.read(min(CHUNK, bundle['size'] - total + 1))
            if not chunk:
                break
            total += len(chunk)
            if total > bundle['size']:
                raise MediaError('Downloaded bundle exceeds registered size.')
            target.write(chunk)
            digest.update(chunk)
    if total != bundle['size'] or digest.hexdigest() != bundle['sha256']:
        raise MediaError('Downloaded bundle size or SHA-256 hash mismatch.')


def _verify_and_stage(data, bundle_path, staging, selected):
    path = Path(bundle_path)
    if not path.is_file() or path.stat().st_size != data['bundle']['size']:
        raise MediaError('Media bundle size mismatch.')
    if file_sha256(path) != data['bundle']['sha256']:
        raise MediaError('Media bundle SHA-256 hash mismatch.')
    inventory = {a['path']: a for a in data['assets']}
    selected_paths = {a['path'] for a in selected}
    with zipfile.ZipFile(path) as archive:
        seen = set()
        for info in archive.infolist():
            name = safe_path(info.filename)
            if name.casefold() in seen:
                raise MediaError(f'duplicate ZIP path: {name}')
            seen.add(name.casefold())
            mode = info.external_attr >> 16
            if info.is_dir() or stat.S_IFMT(mode) not in (0, stat.S_IFREG):
                raise MediaError(f'Refusing directory, symlink or special ZIP entry: {name}')
            if info.flag_bits & 1:
                raise MediaError(f'Refusing encrypted ZIP entry: {name}')
            if name not in inventory:
                raise MediaError(f'Unexpected ZIP entry: {name}')
            if info.file_size != inventory[name]['size']:
                raise MediaError(f'ZIP member size mismatch: {name}')
        if seen != {name.casefold() for name in inventory}:
            raise MediaError('The ZIP does not contain the complete registered inventory.')
        for info in archive.infolist():
            asset = inventory[info.filename]
            digest, total = hashlib.sha256(), 0
            target = Path(staging) / info.filename if info.filename in selected_paths else None
            if target:
                target.parent.mkdir(parents=True, exist_ok=True)
            output = target.open('wb') if target else None
            try:
                with archive.open(info) as source:
                    while True:
                        chunk = source.read(min(CHUNK, asset['size'] - total + 1))
                        if not chunk:
                            break
                        total += len(chunk)
                        if total > asset['size']:
                            raise MediaError(f'ZIP member exceeds registered size: {info.filename}')
                        digest.update(chunk)
                        if output:
                            output.write(chunk)
                if total != asset['size'] or digest.hexdigest() != asset['sha256']:
                    raise MediaError(f'ZIP member SHA-256 hash mismatch: {info.filename}')
            finally:
                if output:
                    output.close()


def _make_parents(path, created):
    missing = []
    cursor = path
    while not cursor.exists():
        missing.append(cursor)
        cursor = cursor.parent
    if not cursor.is_dir():
        raise MediaError(f'Media parent is not a directory: {cursor}')
    for directory in reversed(missing):
        directory.mkdir()
        created.append(directory)


def _install(dest, assets, staging):
    installed, skipped, directories = [], 0, []
    try:
        # Check every selected destination before installing any member.
        for asset in assets:
            target = _target(dest, asset['path'])
            if target.exists() and not _matches(target, asset):
                raise MediaError(f'Refusing to overwrite locally modified media: {asset["path"]}')
        for asset in assets:
            target = _target(dest, asset['path'])
            if target.exists():
                if not _matches(target, asset):
                    raise MediaError(f'Refusing to overwrite locally modified media: {asset["path"]}')
                skipped += 1
                continue
            _make_parents(target.parent, directories)
            _target(dest, asset['path'])
            # A same-directory temporary file plus exclusive hard-link publication
            # gives atomic installation and cannot overwrite a newly appeared file.
            pending = None
            try:
                with tempfile.NamedTemporaryFile(prefix='.motion-media-', dir=target.parent, delete=False) as output:
                    pending = Path(output.name)
                    with (Path(staging) / asset['path']).open('rb') as source:
                        shutil.copyfileobj(source, output, CHUNK)
                    output.flush()
                    os.fsync(output.fileno())
                os.link(pending, target)
                installed.append(target)
            finally:
                if pending:
                    pending.unlink(missing_ok=True)
    except Exception:
        for target in reversed(installed):
            target.unlink(missing_ok=True)
        for directory in reversed(directories):
            try:
                directory.rmdir()
            except OSError:
                pass
        raise
    return {'installed': len(installed), 'skipped': skipped}


def download(manifest_path=DEFAULT_MANIFEST, dest=ROOT, media_set='all', bundle_path=None):
    data = load_manifest(manifest_path)
    selected = _selected(data, media_set)
    for asset in selected:
        target = _target(dest, asset['path'])
        if target.exists() and not _matches(target, asset):
            raise MediaError(f'Refusing to overwrite locally modified media: {asset["path"]}')
    if bundle_path is None and all(_matches(_target(dest, a['path']), a) for a in selected):
        return {'set': media_set, 'installed': 0, 'skipped': len(selected), 'passed': True}
    if bundle_path is None and not data['published']:
        raise MediaError('This media release is not published yet; use --bundle with the prepared local ZIP.')
    with tempfile.TemporaryDirectory(prefix='motion-media-') as folder:
        folder = Path(folder)
        try:
            if bundle_path is None:
                bundle_path = folder / data['bundle']['filename']
                _fetch(data['bundle'], bundle_path)
            _verify_and_stage(data, bundle_path, folder / 'verified', selected)
            result = _install(Path(dest).absolute(), selected, folder / 'verified')
        except (OSError, zipfile.BadZipFile, RuntimeError) as error:
            raise MediaError(f'Cannot safely restore media: {error}') from error
    return {'set': media_set, **result, 'passed': True}


def _tracked_videos(root):
    if not (Path(root) / '.git').exists():
        return []  # Source archives can still package restored registered assets.
    result = subprocess.run(['git', '-C', str(root), 'ls-files', '-z', '--', '*.mp4'],
                            check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return [p for p in result.stdout.decode('utf-8').split('\0') if p]


def _entry(path, content, media_type, media_set):
    return {'path': safe_path(path), 'type': media_type, 'set': media_set,
            'size': len(content), 'sha256': hashlib.sha256(content).hexdigest()}


def pack(root=ROOT, manifest_path=DEFAULT_MANIFEST, output_dir=None, paths=None,
         tag=RELEASE_TAG, includes=()):
    """Package restored inventory, tracked videos and explicitly included new videos.

    A published manifest's tag cannot be reused. Existing registered videos must
    first be restored with download; unregistered export folders are not scanned.
    """
    root = Path(root).resolve()
    manifest_path = Path(manifest_path)
    previous = load_manifest(manifest_path) if manifest_path.exists() else None
    if not isinstance(tag, str) or not re.fullmatch(r'[A-Za-z0-9_.-]+', tag) or tag in ('.', '..'):
        raise MediaError('Invalid media release tag.')
    published_tags = set(previous.get('publishedTags', [])) if previous else set()
    if previous and previous['published']:
        published_tags.add(previous['releaseTag'])
    if tag in published_tags:
        raise MediaError(f'Tag {tag!r} is already published and immutable; choose a new --tag.')
    output_dir = Path(output_dir) if output_dir else root / 'out/media-release'
    tracked = _tracked_videos(root) if paths is None else paths
    registered = [a['path'] for a in previous['assets'] if a['type'] == 'video'] if previous else []
    paths = sorted(set(registered + list(tracked) + list(includes)))
    if not paths:
        raise MediaError('No registered or tracked MP4s to package; use --include for a new local video.')
    contents, inventory = {}, []
    for path in paths:
        path = safe_path(path)
        if not path.endswith('.mp4') or not path.startswith(('examples/', 'media/')):
            raise MediaError(f'Explicit media inclusions must be relative MP4 paths under examples/ or media/: {path}')
        target = _target(root, path)
        if not target.is_file():
            raise MediaError(f'Media video is missing: {path}. Run download --set all first to restore registered media; '
                             'new --include videos must already exist locally.')
        content = target.read_bytes()
        contents[path] = content
        inventory.append(_entry(path, content, 'video',
                                'demos' if path.startswith('examples/capability-demos/') else 'all'))
    notice_prefix = f'media/release-notices/{tag}/'
    notice_text = ('# Motion Diagram Studio media release\n\n'
                   'This bundle restores existing MP4 paths for local previews and GitHub Pages.\n'
                   'LICENSE and THIRD_PARTY_NOTICES.md are snapshots shipped with this media release.\n'
                   'The MIT code license does not grant blanket rights to referenced visual designs,\n'
                   'third-party fonts, source illustrations or recreation videos. See the notices\n'
                   'and source credits before reusing or redistributing individual assets.\n')
    notices = {'README.md': notice_text.encode('utf-8'),
               'LICENSE': (root / 'LICENSE').read_bytes(),
               'THIRD_PARTY_NOTICES.md': (root / 'THIRD_PARTY_NOTICES.md').read_bytes()}
    for name, content in notices.items():
        path = notice_prefix + name
        contents[path] = content
        inventory.append(_entry(path, content, 'metadata', 'all'))
    inventory.sort(key=lambda a: a['path'])
    # Validate input paths/duplicates before packaging; the final bundle descriptor
    # is filled after the deterministic byte stream has been written.
    bundle_name = f'motion-diagram-studio-{tag}.zip'
    data = {'version': 1, 'repository': REPOSITORY, 'releaseTag': tag, 'published': False,
            'publishedTags': sorted(published_tags),
            'bundle': {'filename': bundle_name,
                       'url': f'https://github.com/{REPOSITORY}/releases/download/{tag}/{bundle_name}',
                       'size': 1, 'sha256': '0' * 64}, 'assets': inventory}
    validate_manifest(data)
    output_dir.mkdir(parents=True, exist_ok=True)
    bundle = output_dir / bundle_name
    pending = bundle.with_suffix('.pending.zip')
    try:
        with zipfile.ZipFile(pending, 'w', compression=zipfile.ZIP_STORED, allowZip64=True) as archive:
            for asset in inventory:
                info = zipfile.ZipInfo(asset['path'], date_time=(1980, 1, 1, 0, 0, 0))
                info.create_system = 3
                info.external_attr = (stat.S_IFREG | 0o644) << 16
                info.compress_type = zipfile.ZIP_STORED
                archive.writestr(info, contents[asset['path']])
        data['bundle']['size'] = pending.stat().st_size
        data['bundle']['sha256'] = file_sha256(pending)
        validate_manifest(data)
        os.replace(pending, bundle)
    finally:
        pending.unlink(missing_ok=True)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    result = {'bundlePath': str(bundle.resolve()), 'manifestPath': str(manifest_path.resolve()),
              'releaseTag': tag, 'videoCount': len(paths), 'metadataCount': len(notices),
              'bundleBytes': data['bundle']['size'], 'sha256': data['bundle']['sha256']}
    (output_dir / 'media-release-report.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8', newline='\n')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest='command', required=True)
    package = sub.add_parser('pack', help='Package registered/restored MP4s, tracked MP4s and explicit new videos; no upload.')
    package.add_argument('--manifest', type=Path, default=DEFAULT_MANIFEST)
    package.add_argument('--out', type=Path, default=ROOT / 'out/media-release')
    package.add_argument('--tag', default=RELEASE_TAG, help='New immutable release tag; do not reuse a published tag.')
    package.add_argument('--include', action='append', default=[],
                         help='Explicit new local MP4 path under examples/ or media/; use / separators; repeatable.')
    for command in ('download', 'check'):
        child = sub.add_parser(command)
        child.add_argument('--manifest', type=Path, default=DEFAULT_MANIFEST)
        child.add_argument('--set', choices=('demos', 'all'), default='all', dest='media_set')
        child.add_argument('--dest', type=Path, default=ROOT)
        if command == 'download':
            child.add_argument('--bundle', type=Path, help='Restore from a local ZIP instead of using the network.')
    args = parser.parse_args()
    try:
        if args.command == 'pack':
            result = pack(ROOT, args.manifest, args.out, tag=args.tag, includes=args.include)
        elif args.command == 'download':
            result = download(args.manifest, args.dest, args.media_set, args.bundle)
        else:
            result = check(args.manifest, args.dest, args.media_set)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result.get('passed', True) else 1
    except (MediaError, OSError, subprocess.CalledProcessError) as error:
        parser.exit(1, f'Media error: {error}\n')


if __name__ == '__main__':
    raise SystemExit(main())
