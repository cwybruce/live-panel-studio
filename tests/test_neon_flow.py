"""Real Chrome regression checks for deterministic editorial border neon.

Run after generating the editorial scene configs:
    python -m unittest discover -s tests -p test_neon_flow.py -v
"""
import sys
import tempfile
import unittest
from pathlib import Path
import json

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import livepanel as lp
from check_frames import pixel_diff, TOL_PIXELS


COUNTS = {
    'rag-explainer': 5, 'agent-team': 5, 'product-request': 5,
    'knowledge-card': 5, 'business-workflow': 5, 'incident-replay': 4,
    'component-lab': 6, 'avatar-themes': 4,
}

# Include ancestor opacity: an invisible overlay must not be mistaken for a
# visible child merely because that child's own opacity is one.
ALPHA_JS = """n => {
    let a = 1;
    for (let p=n; p instanceof Element; p=p.parentElement) {
        const s=getComputedStyle(p);
        if (s.display==='none' || s.visibility==='hidden') return 0;
        a *= Number(s.opacity);
    }
    return a;
}"""


class NeonFlowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory(prefix='livepanel-neon-')
        cls.br = lp.Chrome(lp.find_exe(None, lp.CHROME_NAMES, 'Chrome'), 984, 1280)

    @classmethod
    def tearDownClass(cls):
        cls.br.close()
        cls.tmp.cleanup()

    def scene(self, name='rag-explainer', t=1.37, preset=None, **neon):
        folder = lp.ROOT / 'examples/capability-demos' / name
        config = 'config-light.json' if preset == 'light-pastel' else 'config.json'
        cfg = lp.load_config(folder / config)
        options = cfg.setdefault('effects', {}).setdefault('neon', {})
        options.update(enabled=True, intensity=1, period=12, heroPeriod=12)
        options.update(neon)
        path = Path(self.tmp.name) / 'config.json'
        path.write_text(json.dumps(cfg, ensure_ascii=False), encoding='utf-8')
        page = Path(self.tmp.name) / 'live.html'
        lp.build_page(path, page)
        self.br.open(page.as_uri() + '?manual')
        self.br.seek(t)
        self.assertEqual(self.br.eval('window.__error||""'), '')
        return self.br

    def heads(self):
        return self.br.eval('''Array.from(document.querySelectorAll('[data-neon-head]'))
            .map(n=>[Number(n.getAttribute('cx')),Number(n.getAttribute('cy'))])''')

    def source_attributes(self):
        return self.br.eval('''Array.from(document.querySelectorAll('[data-neon-border]'))
            .map(n=>Object.fromEntries(Array.from(n.attributes)
                .map(a=>[a.name,a.value]).sort((a,b)=>a[0].localeCompare(b[0]))))''')

    def test_every_scene_marks_each_border_once(self):
        for name, count in COUNTS.items():
            with self.subTest(scene=name):
                br = self.scene(name)
                actual = br.eval('''({
                    sources:Array.from(document.querySelectorAll('[data-neon-border]'))
                        .map(n=>n.getAttribute('data-neon-border')),
                    layers:Array.from(document.querySelectorAll('[data-neon-layer]'))
                        .map(n=>n.getAttribute('data-neon-layer')),
                    heads:document.querySelectorAll('[data-neon-head]').length
                })''')
                self.assertEqual(len(actual['sources']), count)
                self.assertEqual(len(set(actual['sources'])), count)
                self.assertEqual(sorted(actual['layers']), sorted(actual['sources']))
                self.assertEqual(actual['heads'], count)
                self.assertTrue(all(len(p) == 2 and all(isinstance(v, (int, float))
                                     for v in p) for p in self.heads()))

    def test_disabled_creates_no_overlay(self):
        for name, count in COUNTS.items():
            with self.subTest(scene=name):
                br = self.scene(name, enabled=False)
                self.assertEqual(br.eval('document.querySelectorAll("[data-neon-border]").length'), count)
                self.assertEqual(br.eval('document.querySelectorAll("[data-neon-layer]").length'), 0)
                self.assertEqual(br.eval('document.querySelectorAll("[data-neon-head]").length'), 0)

    def test_replay_restores_attributes_and_pixels(self):
        br = self.scene()
        def state():
            return br.eval('''Array.from(document.querySelectorAll('[data-neon-layer]'))
                .map(n=>n.outerHTML).join('')''')
        first_state, first_heads, first_png = state(), self.heads(), br.shot()
        br.seek(7.91)
        self.assertNotEqual(first_heads, self.heads(), 'neon must move')
        br.seek(1.37)
        self.assertEqual(first_state, state())
        different, delta = pixel_diff(br, first_png, br.shot())
        self.assertLessEqual(different, TOL_PIXELS,
                             f'replay differs: {different} pixels, delta={delta}')

    def test_configured_period_loops_positions_at_twelve_seconds(self):
        for name in COUNTS:
            with self.subTest(scene=name):
                br = self.scene(name, t=0, period=12, heroPeriod=12)
                start = self.heads()
                br.seek(3)
                self.assertNotEqual(start, self.heads())
                br.seek(12)
                end = self.heads()
                self.assertEqual(len(start), len(end))
                for a, b in zip(start, end):
                    for x, y in zip(a, b):
                        self.assertAlmostEqual(x, y, places=5)

    def test_custom_period_changes_position(self):
        self.scene(period=12, heroPeriod=12)
        slow = self.heads()
        self.scene(period=6, heroPeriod=6)
        self.assertNotEqual(slow, self.heads())

    def test_zero_intensity_has_no_visible_heads(self):
        br = self.scene(intensity=0)
        visible = br.eval("Array.from(document.querySelectorAll('[data-neon-head]')).map(" + ALPHA_JS + ")")
        self.assertTrue(all(a == 0 for a in visible), visible)

    def test_light_theme_uses_weaker_halo(self):
        def halo_alpha():
            return self.br.eval("Array.from(document.querySelectorAll('[data-neon-halo]')).map(" + ALPHA_JS + ")")
        self.scene('avatar-themes')
        dark = halo_alpha()
        self.assertTrue(dark, 'generated halo paths need data-neon-halo')
        self.scene('avatar-themes', preset='light-pastel')
        light = halo_alpha()
        self.assertEqual(len(dark), len(light))
        self.assertGreater(sum(dark), 0)
        self.assertLess(sum(light), sum(dark))

    def test_overlay_does_not_change_source_active_styles(self):
        for name in COUNTS:
            with self.subTest(scene=name):
                self.scene(name, t=1.37, enabled=False)
                baseline = self.source_attributes()
                self.scene(name, t=1.37, enabled=True)
                self.assertEqual(baseline, self.source_attributes())
        br = self.scene('rag-explainer', t=1.37)
        first = self.source_attributes()
        br.seek(7.5)
        self.assertNotEqual(first, self.source_attributes(),
                            'RAG active border styling must still follow its stage')


if __name__ == '__main__':
    unittest.main()
