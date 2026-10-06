"""The simulated terminal shell is optional, deterministic and offline."""
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import livepanel as lp
from check_frames import pixel_diff
from verify_capability_demos import editorial_layout, platform_fonts

OUT = lp.ROOT / 'examples/capability-demos'


class TerminalRendererTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((OUT / 'manifest.json').read_text(encoding='utf-8'))
        cls.br = lp.Chrome(lp.find_exe(None, lp.CHROME_NAMES, 'Chrome'), 984, 1280)

    @classmethod
    def tearDownClass(cls):
        cls.br.close()

    def test_original_scenes_keep_their_header_footer_and_no_shell(self):
        for scene in self.manifest:
            with self.subTest(scene=scene['id']):
                self.br.open((OUT / scene['id'] / 'live.html').as_uri() + '?manual')
                self.br.seek(5.3)
                self.assertEqual(self.br.eval('document.querySelectorAll("[data-terminal-shell],[data-terminal-border]").length'), 0)
                self.assertTrue(self.br.eval('Array.from(document.querySelectorAll("[data-diagram-header],[data-diagram-footer]")).every(n=>getComputedStyle(n).display!=="none")'))

    def test_all_scenes_have_ascii_borders_and_advance_simulated_logs(self):
        for scene in self.manifest:
            with self.subTest(scene=scene['id']):
                page = scene['styleVariants']['terminal']['themeVariants']['terminal-classic']['page']
                self.br.open((OUT / scene['id'] / page).as_uri() + '?manual')
                self.br.seek(0)
                self.assertEqual(self.br.eval('document.querySelectorAll("[data-terminal-shell]").length'), 1)
                self.assertEqual(self.br.eval('document.querySelectorAll("[data-terminal-traffic-light]").length'), 3)
                self.assertEqual(self.br.eval('document.querySelectorAll("[data-terminal-border]").length'), len(scene['exportViews']))
                self.assertIn('模拟', self.br.eval('document.querySelector("[data-terminal-log]").textContent'))
                self.assertEqual(self.br.eval('document.querySelector("[data-terminal-command]").textContent'), '')
                self.assertTrue(self.br.eval('Array.from(document.querySelectorAll("[data-terminal-border]")).every(n=>n.textContent.includes("+--")&&n.textContent.includes("|"))'))
                self.br.seek(5.3)
                self.assertIn('python scripts/render.py', self.br.eval('document.querySelector("[data-terminal-command]").textContent'))
                self.assertIn('关键点', self.br.eval('document.querySelector("[data-terminal-shell]").textContent'))
                self.assertEqual(editorial_layout(self.br), [])
                self.assertEqual(self.br.eval('window.__check()'), [])

    def test_four_palettes_use_embedded_fonts_and_reverse_seek_exactly(self):
        scene = self.manifest[0]
        self.assertEqual(scene['id'], 'rag-explainer')
        for theme, files in scene['styleVariants']['terminal']['themeVariants'].items():
            with self.subTest(theme=theme):
                self.br.open((OUT / scene['id'] / files['page']).as_uri() + '?manual')
                self.br.seek(5.3)
                self.assertGreater(platform_fonts(self.br, 'terminal')['chineseTextRunsWithoutSystemFallback'], 10)
                original = self.br.shot()
                self.br.seek(.45)
                self.assertEqual(editorial_layout(self.br), [])
                self.assertGreater(pixel_diff(self.br, original, self.br.shot())[0], 24)
                self.br.seek(5.3)
                self.assertEqual(pixel_diff(self.br, original, self.br.shot())[0], 0)


if __name__ == '__main__':
    unittest.main()
