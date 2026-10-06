"""Restore published media without trusting ZIP paths or overwriting local edits."""
import copy
import hashlib
import json
import stat
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
try:
    import media_assets as media
except ModuleNotFoundError:
    media = None


class MediaBundleTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(media, 'The media restore tool has not been implemented yet.')
        self.temp = tempfile.TemporaryDirectory(prefix='motion-media-test-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / 'source'
        self.source.mkdir()
        self.paths = ['examples/capability-demos/test/demo.mp4', 'media/exports/test/block.mp4']
        for path, content in zip(self.paths, [b'demo video fixture', b'block video fixture']):
            target = self.source / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
        (self.source / 'LICENSE').write_text('MIT license fixture\n', encoding='utf-8')
        (self.source / 'THIRD_PARTY_NOTICES.md').write_text('Fonts and references retain their licenses.\n', encoding='utf-8')
        self.manifest_path = self.root / 'assets-manifest.json'
        self.result = media.pack(self.source, self.manifest_path, self.root / 'release', paths=self.paths)
        self.bundle = Path(self.result['bundlePath'])
        self.manifest = media.load_manifest(self.manifest_path)
        self.dest = self.root / 'restore'

    def save_manifest(self, manifest):
        self.manifest_path.write_text(json.dumps(manifest), encoding='utf-8')

    def altered_bundle(self, extra=None, replace=None):
        target = self.root / 'altered.zip'
        with zipfile.ZipFile(self.bundle) as original, zipfile.ZipFile(target, 'w') as output:
            for info in original.infolist():
                content = original.read(info.filename)
                if replace and info.filename == replace[0]:
                    content = replace[1]
                output.writestr(info, content)
            if extra:
                output.writestr(extra[0], extra[1])
        manifest = copy.deepcopy(self.manifest)
        manifest['bundle']['size'] = target.stat().st_size
        manifest['bundle']['sha256'] = hashlib.sha256(target.read_bytes()).hexdigest()
        self.save_manifest(manifest)
        return target

    def test_restore_selected_demos_and_notice_snapshots(self):
        result = media.download(self.manifest_path, self.dest, 'demos', self.bundle)
        self.assertEqual(result['installed'], 4)  # one video and three notice snapshots
        self.assertEqual((self.dest / self.paths[0]).read_bytes(), (self.source / self.paths[0]).read_bytes())
        self.assertFalse((self.dest / self.paths[1]).exists())
        self.assertTrue((self.dest / 'media/release-notices/media-v1/LICENSE').is_file())
        self.assertTrue(media.check(self.manifest_path, self.dest, 'demos')['passed'])
        self.assertFalse(media.check(self.manifest_path, self.dest, 'all')['passed'])

    def test_skip_matching_files_and_restore_remaining_set(self):
        media.download(self.manifest_path, self.dest, 'demos', self.bundle)
        first = self.dest / self.paths[0]
        before = first.stat().st_mtime_ns
        result = media.download(self.manifest_path, self.dest, 'all', self.bundle)
        self.assertEqual(result['installed'], 1)
        self.assertEqual(result['skipped'], 4)
        self.assertEqual(first.stat().st_mtime_ns, before)
        self.assertTrue(media.check(self.manifest_path, self.dest, 'all')['passed'])

    def test_pack_is_reproducible_independent_of_input_order_and_mtime(self):
        before = self.bundle.read_bytes()
        import os
        os.utime(self.source / self.paths[0], (100000, 100000))
        other = media.pack(self.source, self.root / 'other.json', self.root / 'other-release', paths=self.paths[::-1])
        self.assertEqual(before, Path(other['bundlePath']).read_bytes())

    def test_bundle_hash_mismatch_creates_no_destination(self):
        broken = self.root / 'broken.zip'
        broken.write_bytes(self.bundle.read_bytes()[:-1] + b'!')
        with self.assertRaisesRegex(media.MediaError, 'hash|SHA'):
            media.download(self.manifest_path, self.dest, 'all', broken)
        self.assertFalse(self.dest.exists())

    def test_member_hash_mismatch_creates_no_destination(self):
        broken = self.altered_bundle(replace=(self.paths[1], b'other video fixture'))
        with self.assertRaisesRegex(media.MediaError, 'hash|SHA|size'):
            media.download(self.manifest_path, self.dest, 'demos', broken)
        self.assertFalse(self.dest.exists())  # unselected files are validated too

    def test_existing_modified_video_prevents_any_other_install(self):
        target = self.dest / self.paths[1]
        target.parent.mkdir(parents=True)
        target.write_bytes(b'my edited video')
        before = {p.relative_to(self.dest).as_posix(): p.read_bytes()
                  for p in self.dest.rglob('*') if p.is_file()}
        with self.assertRaisesRegex(media.MediaError, 'modified|overwrite'):
            media.download(self.manifest_path, self.dest, 'all', self.bundle)
        after = {p.relative_to(self.dest).as_posix(): p.read_bytes()
                 for p in self.dest.rglob('*') if p.is_file()}
        self.assertEqual(before, after)

    def test_unsafe_manifest_paths_are_rejected(self):
        for unsafe in ['../escape.mp4', '/escape.mp4', 'C:/escape.mp4', 'folder\\escape.mp4',
                       'folder/../escape.mp4', 'folder//escape.mp4', 'folder/file.mp4:stream', 'CON.mp4']:
            with self.subTest(path=unsafe):
                changed = copy.deepcopy(self.manifest)
                changed['assets'][0]['path'] = unsafe
                self.save_manifest(changed)
                with self.assertRaises(media.MediaError):
                    media.load_manifest(self.manifest_path)
        self.assertFalse(self.dest.exists())

    def test_duplicate_manifest_paths_are_rejected(self):
        changed = copy.deepcopy(self.manifest)
        changed['assets'].append(copy.deepcopy(changed['assets'][0]))
        self.save_manifest(changed)
        with self.assertRaisesRegex(media.MediaError, 'duplicate'):
            media.load_manifest(self.manifest_path)

    def test_zip_traversal_and_unexpected_entries_are_rejected(self):
        for unsafe in ['../escape.mp4', 'extra.mp4', 'folder\\escape.mp4']:
            with self.subTest(path=unsafe):
                broken = self.altered_bundle(extra=(unsafe, b'unsafe'))
                with self.assertRaises(media.MediaError):
                    media.download(self.manifest_path, self.dest, 'all', broken)
                self.assertFalse(self.dest.exists())

    def test_duplicate_zip_entries_are_rejected(self):
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', UserWarning)
            broken = self.altered_bundle(extra=(self.paths[0], b'duplicate'))
        with self.assertRaisesRegex(media.MediaError, 'duplicate'):
            media.download(self.manifest_path, self.dest, 'all', broken)
        self.assertFalse(self.dest.exists())

    def test_zip_symlink_entries_are_rejected(self):
        info = zipfile.ZipInfo('link.mp4')
        info.create_system = 3
        info.external_attr = (stat.S_IFLNK | 0o777) << 16
        broken = self.altered_bundle(extra=(info, b'../outside'))
        with self.assertRaises(media.MediaError):
            media.download(self.manifest_path, self.dest, 'all', broken)
        self.assertFalse(self.dest.exists())

    def test_destination_symlink_is_rejected_when_available(self):
        outside = self.root / 'outside'
        outside.mkdir()
        try:
            self.dest.symlink_to(outside, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest('The host does not permit symlink creation.')
        with self.assertRaisesRegex(media.MediaError, 'symlink|outside'):
            media.download(self.manifest_path, self.dest, 'all', self.bundle)
        self.assertEqual(list(outside.iterdir()), [])

    def test_published_paths_requires_publication_and_ignores_metadata(self):
        self.assertTrue(hasattr(media, 'published_paths'), 'Published-path lookup is not implemented yet.')
        self.assertEqual(media.published_paths(self.root / 'missing.json'), set())
        self.assertEqual(media.published_paths(self.manifest_path), set())
        self.manifest['published'] = True
        self.save_manifest(self.manifest)
        self.assertEqual(media.published_paths(self.manifest_path), set(self.paths))
        self.manifest['assets'][0]['path'] = '../unsafe.mp4'
        self.save_manifest(self.manifest)
        with self.assertRaises(media.MediaError):
            media.published_paths(self.manifest_path)

    def test_install_failure_rolls_back_already_installed_files(self):
        from unittest.mock import patch
        original_link = media.os.link
        calls = []

        def fail_second(source, destination):
            calls.append(str(destination))
            if len(calls) == 2:
                raise OSError('fixture filesystem failure')
            return original_link(source, destination)

        with patch.object(media.os, 'link', side_effect=fail_second):
            with self.assertRaisesRegex(media.MediaError, 'fixture filesystem failure'):
                media.download(self.manifest_path, self.dest, 'all', self.bundle)
        self.assertFalse(self.dest.exists())

    def test_staging_copy_failure_leaves_no_partial_destination(self):
        from unittest.mock import patch

        def fail_copy(source, destination, length):
            destination.write(source.read(1))
            raise OSError('fixture copy failure')

        with patch.object(media.shutil, 'copyfileobj', side_effect=fail_copy):
            with self.assertRaisesRegex(media.MediaError, 'fixture copy failure'):
                media.download(self.manifest_path, self.dest, 'all', self.bundle)
        self.assertFalse(self.dest.exists())

    def test_network_download_rejects_excess_or_truncated_bytes(self):
        import io
        from unittest.mock import patch

        class Response(io.BytesIO):
            headers = {}

        for content in (self.bundle.read_bytes() + b'excess', self.bundle.read_bytes()[:-3]):
            with self.subTest(size=len(content)):
                self.manifest['published'] = True
                self.save_manifest(self.manifest)
                with patch.object(media.urllib.request, 'urlopen', return_value=Response(content)):
                    with self.assertRaisesRegex(media.MediaError, 'size|hash'):
                        media.download(self.manifest_path, self.dest, 'all')
                self.assertFalse(self.dest.exists())

    def test_network_timeout_creates_no_destination(self):
        from unittest.mock import patch
        self.manifest['published'] = True
        self.save_manifest(self.manifest)
        with patch.object(media.urllib.request, 'urlopen', side_effect=TimeoutError('fixture timeout')):
            with self.assertRaises((media.MediaError, TimeoutError)):
                media.download(self.manifest_path, self.dest, 'all')
        self.assertFalse(self.dest.exists())

    def test_new_release_packages_restored_inventory_without_tracked_mp4s(self):
        import inspect
        from unittest.mock import patch
        self.assertIn('tag', inspect.signature(media.pack).parameters,
                      'Packaging a new immutable media version is not implemented yet.')
        self.manifest['published'] = True
        self.save_manifest(self.manifest)
        with patch.object(media, '_tracked_videos', return_value=[]):
            result = media.pack(self.source, self.manifest_path, self.root / 'v2', tag='media-v2')
        current = media.load_manifest(self.manifest_path)
        self.assertEqual({a['path'] for a in current['assets'] if a['type'] == 'video'}, set(self.paths))
        self.assertFalse(current['published'])
        self.assertEqual(current['releaseTag'], 'media-v2')
        self.assertEqual(Path(result['bundlePath']).name, 'motion-diagram-studio-media-v2.zip')
        self.assertTrue(all(a['path'].startswith('media/release-notices/media-v2/')
                            for a in current['assets'] if a['type'] == 'metadata'))
        restored = self.root / 'v2-restore'
        media.download(self.manifest_path, restored, 'all', result['bundlePath'])
        self.assertTrue(media.check(self.manifest_path, restored, 'all')['passed'])

    def test_published_release_tag_cannot_be_repackaged(self):
        self.manifest['published'] = True
        self.save_manifest(self.manifest)
        before_bundle = self.bundle.read_bytes()
        before_manifest = self.manifest_path.read_bytes()
        with self.assertRaisesRegex(media.MediaError, 'published|immutable|tag'):
            media.pack(self.source, self.manifest_path, self.bundle.parent, paths=self.paths)
        self.assertEqual(self.bundle.read_bytes(), before_bundle)
        self.assertEqual(self.manifest_path.read_bytes(), before_manifest)

    def test_previous_published_tag_is_remembered_when_preparing_next_version(self):
        from unittest.mock import patch
        self.manifest['published'] = True
        self.save_manifest(self.manifest)
        with patch.object(media, '_tracked_videos', return_value=[]):
            media.pack(self.source, self.manifest_path, self.root / 'next-version', tag='media-v2')
            with self.assertRaisesRegex(media.MediaError, 'published|immutable|tag'):
                media.pack(self.source, self.manifest_path, self.bundle.parent, tag='media-v1')
        self.assertEqual(media.load_manifest(self.manifest_path)['publishedTags'], ['media-v1'])

    def test_explicit_include_adds_new_video_without_scanning_user_exports(self):
        import inspect
        from unittest.mock import patch
        self.assertIn('includes', inspect.signature(media.pack).parameters,
                      'Explicit new media inclusion is not implemented yet.')
        included = 'examples/new-demo/demo.mp4'
        excluded = 'examples/capability-demos/exports/private.mp4'
        for relative in (included, excluded):
            target = self.source / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(b'new local video')
        with patch.object(media, '_tracked_videos', return_value=[]):
            media.pack(self.source, self.manifest_path, self.root / 'with-new',
                       tag='media-v2', includes=[included])
        registered = {a['path'] for a in media.load_manifest(self.manifest_path)['assets'] if a['type'] == 'video'}
        self.assertEqual(registered, set(self.paths + [included]))
        self.assertNotIn(excluded, registered)

    def test_unsafe_or_nonvideo_explicit_includes_are_rejected(self):
        import inspect
        from unittest.mock import patch
        self.assertIn('includes', inspect.signature(media.pack).parameters)
        for path in ('../outside.mp4', 'examples\\outside.mp4', 'C:/outside.mp4', 'scripts/code.py'):
            with self.subTest(path=path), patch.object(media, '_tracked_videos', return_value=[]):
                with self.assertRaises(media.MediaError):
                    media.pack(self.source, self.manifest_path, self.root / 'unsafe-include',
                               tag='media-v2', includes=[path])
        self.assertFalse((self.root / 'unsafe-include').exists())

    def test_missing_inventory_video_explains_restore_before_repackaging(self):
        import inspect
        from unittest.mock import patch
        self.assertIn('tag', inspect.signature(media.pack).parameters)
        (self.source / self.paths[1]).unlink()
        with patch.object(media, '_tracked_videos', return_value=[]):
            with self.assertRaisesRegex(media.MediaError, 'download'):
                media.pack(self.source, self.manifest_path, self.root / 'missing-video', tag='media-v2')
        self.assertFalse((self.root / 'missing-video').exists())


class PublishedInventoryTests(unittest.TestCase):
    def test_current_inventory_contains_all_eighty_videos_and_thirty_two_demos(self):
        self.assertIsNotNone(media, 'The media restore tool has not been implemented yet.')
        inventory = media.load_manifest(ROOT / 'media/assets-manifest.json')
        videos = [a for a in inventory['assets'] if a['type'] == 'video']
        self.assertEqual(len(videos), 80)
        self.assertEqual(sum(a['set'] == 'demos' for a in videos), 32)
        self.assertEqual(sum(a['size'] for a in videos), 56566395)
        self.assertFalse(any('national-day-promo' in a['path'] for a in videos))
        self.assertEqual(inventory['bundle']['url'],
                         'https://github.com/cwybruce/motion-diagram-studio/releases/download/media-v2/motion-diagram-studio-media-v2.zip')
        for asset in videos:
            path = ROOT / asset['path']
            if path.is_file():  # fresh source checkouts intentionally do not contain MP4s
                self.assertEqual(media.file_sha256(path), asset['sha256'], asset['path'])


if __name__ == '__main__':
    unittest.main()
