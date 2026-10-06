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
    def test_text_colors_remain_readable_on_all_palette_surfaces(self):
        def luminance(color):
            rgb = [int(color[i:i+2], 16) / 255 for i in (1, 3, 5)]
            linear = [v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in rgb]
            return sum(v * w for v, w in zip(linear, (.2126, .7152, .0722)))

        for theme, colors in demos.EDITORIAL_PALETTES.items():
            for role in ('fg', 'dim', 'amber', 'cyan', 'pink', 'mint', 'red', 'bl'):
                for surface in ('bg', 'panel', 'surface'):
                    with self.subTest(theme=theme, role=role, surface=surface):
                        a, b = sorted((luminance(colors[role]), luminance(colors[surface])))
                        self.assertGreaterEqual((b + .05) / (a + .05), 7 if role == 'fg' else 4.5)

    def test_variants_preserve_scene_timing_geometry_and_source(self):
        original = lp.load_config(ed.DEMO_ROOT / 'rag-explainer/config.json')
        before = copy.deepcopy(original)
        expected = {'terminal-dark': ('terminal-dark', '#191713'),
                    'light-pastel': ('light-pastel', '#faf7f0'),
                    'terminal-classic': ('terminal-dark', '#191f27'),
                    'pastel-classic': ('light-pastel', '#ffffff')}
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
        if t is not None:
            self.browser.seek(t)
        return self.browser

    def test_warm_palette_repeated_seek_preserves_original_color_roles(self):
        br = self.scene('component-lab', 'terminal-dark', t=None)
        palette = demos.EDITORIAL_PALETTES['terminal-dark']
        leader = '''document.querySelector('[data-component="seats"] > g[transform="translate(300 13) scale(0.65)"]')'''
        self.assertEqual(br.eval(leader + '.getAttribute("stroke")'), palette['bg'])
        first = br.shot()
        for time in (0, 9.25, 0):
            br.seek(time)
            self.assertEqual(br.eval(leader + '.getAttribute("stroke")'), palette['bg'])
        self.assertEqual(first, br.shot())

        # Animated attributes are rewritten by draw callbacks before recoloring.
        ticket = '''document.querySelector('[data-component="kanban"] > g > rect')'''
        for time, role in ((0, 'dim'), (3.25, 'amber'), (6.25, 'blue'), (9.25, 'mint')):
            br.seek(time)
            self.assertEqual(br.eval(ticket + '.getAttribute("stroke")'), palette[role])

        # A new node and a new authored token must not inherit stale mapping.
        br.eval('''(()=>{
            const root=document.querySelector('[data-component="seats"]');
            const node=document.createElementNS('http://www.w3.org/2000/svg','circle');
            node.id='palette-regression-node';node.setAttribute('fill','#211a13');
            root.appendChild(node);
        })()''')
        for time in (0, 0, 9.25, 0):
            br.seek(time)
            self.assertEqual(br.eval('document.getElementById("palette-regression-node").getAttribute("fill")'), palette['bg'])
        br.eval('document.getElementById("palette-regression-node").setAttribute("fill", "#53b9c5")')
        br.seek(0)
        self.assertEqual(br.eval('document.getElementById("palette-regression-node").getAttribute("fill")'), palette['cyan'])
        br.seek(0)
        self.assertEqual(br.eval('document.getElementById("palette-regression-node").getAttribute("fill")'), palette['cyan'])

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
