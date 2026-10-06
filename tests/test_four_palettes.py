"""Four palette variants keep scene data stable and export the chosen palette.

Pure tests use temporary trusted metadata, so they can run before regeneration.
Browser tests build isolated pages from the checked-in authored scene configs.
"""
import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import export_demo as ed
import livepanel as lp
import make_capability_demos as demos


class FourPaletteConfigTests(unittest.TestCase):
    def test_variants_preserve_scene_timing_geometry_and_source(self):
        original = lp.load_config(ed.DEMO_ROOT / 'rag-explainer/config.json')
        before = copy.deepcopy(original)
        expected = {'terminal-dark': ('terminal-dark', '#12110f'),
                    'light-pastel': ('light-pastel', '#f1eee5'),
                    'terminal-classic': ('terminal-dark', '#14171c'),
                    'pastel-classic': ('light-pastel', '#fcfcfb')}
        self.assertEqual(set(expected), set(ed.THEMES))
        for theme, (preset, background) in expected.items():
            with self.subTest(theme=theme):
                version = demos.theme_config(original, theme)
                self.assertEqual(version['theme']['variant'], theme)
                self.assertEqual(version['theme']['preset'], preset)
                self.assertEqual(version['theme']['colors']['bg'], background)
                for field in ('canvas', 'machines', 'elements', 'effects'):
                    self.assertEqual(version[field], original[field])
        self.assertEqual(original, before)

    def test_legacy_render_selection_and_unique_new_filenames(self):
        self.assertEqual(demos.render_themes('both'), ['terminal-dark', 'light-pastel'])
        self.assertEqual(demos.render_themes('terminal'), ['terminal-classic'])
        self.assertEqual(demos.render_themes('pastel'), ['pastel-classic'])
        self.assertEqual(set(demos.render_themes('all')), set(ed.THEMES))
        for role in ('config', 'page', 'video', 'poster'):
            self.assertEqual(len({m[role] for m in demos.THEME_VARIANTS.values()}), 4)
        self.assertEqual(demos.THEME_VARIANTS['terminal-dark']['video'], 'demo.mp4')
        self.assertEqual(demos.THEME_VARIANTS['light-pastel']['video'], 'demo-light.mp4')
        self.assertEqual(ed.THEME_CONFIGS,
                         {k: m['config'] for k, m in demos.THEME_VARIANTS.items()})

    def test_exact_export_variant_and_no_missing_classic_fallback(self):
        original = lp.load_config(ed.DEMO_ROOT / 'rag-explainer/config.json')
        with tempfile.TemporaryDirectory(prefix='lp-four-themes-') as temp:
            root = Path(temp)
            folder = root / 'rag-explainer'
            folder.mkdir()
            (root / 'manifest.json').write_text(json.dumps([
                {'id': 'rag-explainer', 'exportViews': [
                    {'id': 'rag-test', 'crop': [20, 30, 200, 100]}]}]), encoding='utf-8')
            for theme, metadata in demos.THEME_VARIANTS.items():
                version = demos.theme_config(original, theme)
                version['meta']['paletteEvidence'] = theme
                (folder / metadata['config']).write_text(json.dumps(version), encoding='utf-8')
            for theme in ed.THEMES:
                with self.subTest(theme=theme):
                    spec = ed.validate_request({'scene': 'rag-explainer', 'theme': theme,
                                                'avatar': 'drone', 'view': 'rag-test'}, root)
                    self.assertEqual(spec.config['meta']['paletteEvidence'], theme)
                    self.assertEqual(spec.config['theme']['variant'], theme)
                    self.assertEqual(spec.crop, (20, 30, 200, 100))
                    self.assertIn(theme, spec.filename)
            (folder / 'config-terminal.json').unlink()
            with self.assertRaisesRegex(ValueError, '尚未准备好'):
                ed.validate_request({'scene': 'rag-explainer', 'theme': 'terminal-classic'}, root)
            wrong = demos.theme_config(original, 'terminal-dark')
            (folder / 'config-terminal.json').write_text(json.dumps(wrong), encoding='utf-8')
            with self.assertRaisesRegex(ValueError, '不一致'):
                ed.validate_request({'scene': 'rag-explainer', 'theme': 'terminal-classic'}, root)


class FourPaletteBrowserTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='lp-four-palette-browser-')
        cls.browser = lp.Chrome(lp.find_exe(None, lp.CHROME_NAMES, 'Chrome'), 984, 1280)

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.temp.cleanup()

    def scene(self, scene, theme, t=4.5):
        source = lp.load_config(ed.DEMO_ROOT / scene / 'config.json')
        config = demos.theme_config(source, theme)
        path = Path(self.temp.name) / 'config.json'
        page = Path(self.temp.name) / 'live.html'
        path.write_text(json.dumps(config, ensure_ascii=False), encoding='utf-8')
        lp.build_page(path, page)
        self.browser.open(page.as_uri() + '?manual')
        self.browser.seek(t)
        return self.browser

    def test_classic_dark_and_light_recolor_components_and_keep_replay(self):
        for theme in ('terminal-classic', 'pastel-classic'):
            with self.subTest(theme=theme):
                br = self.scene('component-lab', theme)
                palette = demos.EDITORIAL_PALETTES[theme]
                measured = br.eval('''(()=>({
                    background:document.querySelector('[data-component="labEditorial"] > rect').getAttribute('fill'),
                    label:document.querySelector('[data-component="orb"] > text').getAttribute('fill'),
                    subtitle:document.querySelectorAll('[data-component="orb"] > text')[1].getAttribute('fill'),
                    errors:window.__error||'',
                    neon:document.querySelectorAll('[data-neon-layer]').length,
                    originalWarm:Array.from(document.querySelectorAll('[data-component="orb"] [fill],[data-component="seats"] [stroke]'))
                         .some(n=>['#d5d4ce','#53b9c5','#636668'].includes(n.getAttribute('fill')||n.getAttribute('stroke')))
                }))()''')
                self.assertEqual(measured['background'], palette['bg'])
                self.assertEqual(measured['label'], palette['cyan'])
                self.assertEqual(measured['subtitle'], palette['fg'])
                self.assertFalse(measured['originalWarm'])
                self.assertEqual(measured['errors'], '')
                self.assertEqual(measured['neon'], 6)
                first = br.shot()
                br.seek(9)
                self.assertNotEqual(first, br.shot())
                br.seek(4.5)
                self.assertEqual(first, br.shot())

    def test_classic_avatar_authored_colors_map_to_semantic_roles(self):
        for theme in ('terminal-classic', 'pastel-classic'):
            with self.subTest(theme=theme):
                br = self.scene('rag-explainer', theme)
                palette = demos.EDITORIAL_PALETTES[theme]
                colors = br.eval('''(()=>({
                    leg:document.querySelector('[data-spider-leg] > path').getAttribute('stroke'),
                    shell:document.querySelector('[data-spider-body] > path').getAttribute('stroke'),
                    core:document.querySelector('[data-spider-body] > circle').getAttribute('fill')
                }))()''')
                self.assertEqual(colors['leg'], palette['red'])
                self.assertEqual(colors['shell'], palette['pink'])
                self.assertEqual(colors['core'], palette['pink'])


if __name__ == '__main__':
    unittest.main()
