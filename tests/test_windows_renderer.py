"""Integration checks for actual Windows Chromium rendering (no mocked browser)."""
import sys
import json
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import livepanel as lp
from check_frames import pixel_diff, TOL_PIXELS


class RendererTests(unittest.TestCase):
    def test_spider_has_eight_articulated_legs_and_replays(self):
        import tempfile
        cfg = json.loads((lp.ROOT / 'examples/capability-demos/avatar-themes/config.json').read_text(encoding='utf-8'))
        actor = next(e for e in cfg['elements'] if e['type'] == 'drone')
        actor['avatar'] = 'spider'
        with tempfile.TemporaryDirectory() as tmp:
            config = Path(tmp) / 'spider.json'
            config.write_text(json.dumps(cfg), encoding='utf-8')
            page = Path(tmp) / 'spider.html'
            lp.build_page(config, page)
            with lp.Chrome(lp.find_exe(None, lp.CHROME_NAMES, 'Chrome'), 984, 1280) as br:
                br.open(page.as_uri() + '?manual')
                self.assertEqual(br.eval('document.querySelectorAll("[data-spider-leg]").length'), 8)
                self.assertEqual(br.eval('document.querySelector("[data-avatar=spider]").style.display'), '')
                def legs(t):
                    br.seek(t)
                    return br.eval('Array.from(document.querySelectorAll("[data-spider-leg]")).map(n=>n.innerHTML).join("")')
                a = legs(3.25)
                self.assertNotEqual(a, legs(3.55), 'legs must step')
                legs(9.75)
                self.assertEqual(a, legs(3.25), 'gait must replay without accumulated state')
                self.assertEqual(br.eval('window.setAvatar("drone")'), 'drone')
                self.assertEqual(br.eval('document.querySelector("[data-avatar=spider]").style.display'), 'none')
                self.assertEqual(br.eval('window.setAvatar("spider")'), 'spider')
                self.assertEqual(br.eval('window.__error||""'), '')

    def test_original_components_render_and_replay(self):
        import tempfile
        cfg = lp.ROOT / 'examples/capability-demos/component-lab/config.json'
        with tempfile.TemporaryDirectory() as tmp:
            page = Path(tmp) / 'components.html'
            lp.build_page(cfg, page)
            with lp.Chrome(lp.find_exe(None, lp.CHROME_NAMES, 'Chrome'), 984, 1280) as br:
                br.open(page.as_uri() + '?manual')
                def state(t):
                    br.seek(t)
                    return br.eval('document.querySelector("[data-component=seats]").innerHTML + document.querySelector("[data-component=kanban]").innerHTML + document.querySelector("[data-component=donut]").innerHTML')
                a = state(3.25)
                self.assertIn('已选', a)
                self.assertIn('工单01', a)
                self.assertNotEqual(a, state(9.75))
                self.assertEqual(a, state(3.25))
                self.assertEqual(br.eval('window.__error||""'), '')
                self.assertEqual(br.eval('window.__check()'), [])

    def test_chromium_seek_and_screenshot(self):
        import tempfile
        cfg = lp.ROOT / 'examples/codex-agents/config.json'
        with tempfile.TemporaryDirectory() as tmp:
            page = Path(tmp) / 'a page.html'
            lp.build_page(cfg, page)
            with lp.Chrome(lp.find_exe(None, lp.CHROME_NAMES, 'Chrome'), 600, 750) as br:
                br.open(page.as_uri() + '?manual')
                br.seek(2.75)
                a = br.shot()
                br.seek(9)
                b = br.shot()
                br.seek(2.75)
                again = br.shot()
                self.assertTrue(a.startswith(b'\x89PNG'))
                self.assertNotEqual(a, b, 'timeline must animate')
                different, delta = pixel_diff(br, a, again)
                self.assertLessEqual(different, TOL_PIXELS, f'replay differs: {different} pixels, delta={delta}')
                self.assertEqual(br.eval('window.__error||""'), '')


if __name__ == '__main__':
    unittest.main()
