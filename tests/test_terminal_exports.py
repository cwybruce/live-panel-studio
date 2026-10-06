"""Validate display style independently from palettes, using isolated fixtures."""
import contextlib
import http.client
import io
import json
from pathlib import Path
import sys
import tempfile
import threading
import time
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import export_demo as ed
import preview_server as ps


CONSOLE_CONFIGS = {'terminal-dark': 'config-console-dark.json',
                   'light-pastel': 'config-console-light.json',
                   'terminal-classic': 'config-console-terminal.json',
                   'pastel-classic': 'config-console-pastel.json'}


def fixture(root):
    (root / 'index.html').write_text('<!doctype html><title>Style fixture</title>', encoding='utf-8')
    folder = root / 'rag-explainer'
    folder.mkdir()
    themes = {}
    for theme in ed.THEMES:
        config = {'canvas': {'width': 984, 'height': 1280, 'duration': 12, 'fps': 30},
                  'theme': {'preset': ed.THEME_PRESETS[theme], 'variant': theme},
                  'elements': [{'type': 'drone', 'avatar': 'spider'}]}
        (folder / ed.THEME_CONFIGS[theme]).write_text(json.dumps(config), encoding='utf-8')
        config['presentation'] = {'style': 'terminal'}
        (folder / CONSOLE_CONFIGS[theme]).write_text(json.dumps(config), encoding='utf-8')
        themes[theme] = {'config': CONSOLE_CONFIGS[theme]}
    manifest = [{'id': 'rag-explainer', 'exportViews': [{'id': 'rag-hero', 'crop': [16, 180, 952, 380]}],
                 'styleVariants': {'diagram': {'themeVariants': {theme: {'config': name}
                                                                for theme, name in ed.THEME_CONFIGS.items()}},
                                   'terminal': {'themeVariants': themes}}}]
    (root / 'manifest.json').write_text(json.dumps(manifest), encoding='utf-8')
    return folder


class TerminalRequestTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='mds-terminal-request-')
        self.root = Path(self.temporary.name)
        self.folder = fixture(self.root)

    def tearDown(self):
        self.temporary.cleanup()

    def test_terminal_style_keeps_theme_avatar_and_crop_independent(self):
        for theme in ed.THEMES:
            for avatar in ed.AVATARS:
                with self.subTest(theme=theme, avatar=avatar):
                    spec = ed.validate_request({'scene': 'rag-explainer', 'theme': theme,
                                                'style': 'terminal', 'avatar': avatar,
                                                'view': 'rag-hero'}, self.root)
                    self.assertEqual(spec.style, 'terminal')
                    self.assertEqual(spec.config['presentation']['style'], 'terminal')
                    self.assertEqual(spec.config['theme']['variant'], theme)
                    self.assertEqual(spec.config['elements'][0]['avatar'], avatar)
                    self.assertEqual(spec.crop, (16, 180, 952, 380))
                    self.assertEqual(spec.filename, f'rag-explainer-terminal-{theme}-{avatar}-rag-hero.mp4')
                    original = json.loads((self.folder / CONSOLE_CONFIGS[theme]).read_text(encoding='utf-8'))
                    self.assertEqual(original['elements'][0]['avatar'], 'spider')

    def test_default_diagram_preserves_old_config_and_filename(self):
        default = ed.validate_request({'scene': 'rag-explainer'}, self.root)
        explicit = ed.validate_request({'scene': 'rag-explainer', 'style': 'diagram'}, self.root)
        self.assertEqual(default.style, 'diagram')
        self.assertEqual(default.filename, 'rag-explainer-terminal-dark-spider-full.mp4')
        self.assertEqual(default, explicit)

    def test_reject_unlisted_or_mismatched_style(self):
        for style in ('../terminal', 'macos', None, [], 'terminal;whoami'):
            with self.subTest(style=style), self.assertRaises(ValueError):
                ed.validate_request({'scene': 'rag-explainer', 'style': style}, self.root)
        path = self.folder / CONSOLE_CONFIGS['terminal-dark']
        config = json.loads(path.read_text(encoding='utf-8'))
        config['presentation']['style'] = 'diagram'
        path.write_text(json.dumps(config), encoding='utf-8')
        with self.assertRaisesRegex(ValueError, '样式'):
            ed.validate_request({'scene': 'rag-explainer', 'style': 'terminal'}, self.root)
        path.unlink()
        with self.assertRaises(ValueError):
            ed.validate_request({'scene': 'rag-explainer', 'style': 'terminal'}, self.root)

    def test_cli_forwards_style(self):
        spec = ed.validate_request({'scene': 'rag-explainer', 'style': 'terminal'}, self.root)
        with patch.object(sys, 'argv', ['export_demo.py', '--scene', 'rag-explainer', '--style', 'terminal',
                                      '--out', str(self.root / 'terminal.mp4')]), \
                patch.object(ed, 'validate_request', return_value=spec) as validate, \
                patch.object(ed, 'export', return_value={'frames': 360}), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(ed.main(), 0)
        self.assertEqual(validate.call_args.args[0]['style'], 'terminal')

    def test_terminal_style_requires_matching_registered_config(self):
        path = self.root / 'manifest.json'
        original = json.loads(path.read_text(encoding='utf-8'))
        for terminal in ({}, [], {'themeVariants': {'terminal-dark': {'config': '../config.json'}}}):
            changed = json.loads(json.dumps(original))
            changed[0]['styleVariants']['terminal'] = terminal
            path.write_text(json.dumps(changed), encoding='utf-8')
            with self.subTest(terminal=terminal), self.assertRaises(ValueError):
                ed.validate_request({'scene': 'rag-explainer', 'style': 'terminal'}, self.root)


class TerminalApiTests(unittest.TestCase):
    def test_api_returns_selected_style_and_preserves_single_worker(self):
        with tempfile.TemporaryDirectory(prefix='mds-terminal-api-') as directory:
            root = Path(directory)
            fixture(root)
            worker_ids = set()
            def mock_export(spec, output, progress):
                worker_ids.add(threading.get_ident())
                self.assertEqual(spec.config['presentation']['style'], 'terminal')
                output.parent.mkdir(exist_ok=True)
                output.write_bytes(b'terminal-test-video')
                return {'width': spec.width, 'height': spec.height, 'frames': 360}
            with patch.object(ps, 'export', side_effect=mock_export):
                server = ps.make_server(0, root)
                jobs = server.RequestHandlerClass.keywords['exports']
                thread = threading.Thread(target=server.serve_forever, daemon=True)
                thread.start()
                port = server.server_port
                def request(method, path, payload=None):
                    connection = http.client.HTTPConnection('127.0.0.1', port, timeout=5)
                    headers = {'Host': f'127.0.0.1:{port}', 'Origin': f'http://127.0.0.1:{port}',
                               'Sec-Fetch-Site': 'same-origin', 'Content-Type': 'application/json'}
                    try:
                        body = json.dumps(payload).encode('utf-8') if payload is not None else None
                        connection.request(method, path, body, headers)
                        response = connection.getresponse()
                        return response.status, json.loads(response.read())
                    finally:
                        connection.close()
                try:
                    status, job = request('POST', '/api/exports', {'scene': 'rag-explainer', 'style': 'terminal'})
                    self.assertEqual(status, 202)
                    self.assertEqual(job['style'], 'terminal')
                    self.assertEqual(job['filename'], 'rag-explainer-terminal-terminal-dark-spider-full.mp4')
                    deadline = time.monotonic() + 5
                    while job['status'] not in ('complete', 'failed') and time.monotonic() < deadline:
                        time.sleep(.01)
                        status, job = request('GET', '/api/exports/' + job['id'])
                    self.assertEqual(job['status'], 'complete')
                    self.assertEqual(len(worker_ids), 1)
                    status, _ = request('POST', '/api/exports', {'scene': 'rag-explainer', 'style': '../terminal'})
                    self.assertEqual(status, 400)
                finally:
                    jobs.pending.join()
                    server.shutdown()
                    server.server_close()
                    thread.join(timeout=5)


if __name__ == '__main__':
    unittest.main()
