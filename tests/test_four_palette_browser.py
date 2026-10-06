"""Check real palette rendering, gallery state, and published media paths."""
import functools
import json
import sys
import threading
import unittest
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import livepanel as lp
from check_frames import pixel_diff
from verify_capability_demos import editorial_layout, wait_gallery

OUT = lp.ROOT / 'examples/capability-demos'
BACKGROUNDS = {'terminal-dark': 'rgb(18, 17, 15)',
               'light-pastel': 'rgb(241, 238, 229)',
               'terminal-classic': 'rgb(20, 23, 28)',
               'pastel-classic': 'rgb(252, 252, 251)'}


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


class FourPaletteBrowserTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((OUT / 'manifest.json').read_text(encoding='utf-8'))
        cls.br = lp.Chrome(lp.find_exe(None, lp.CHROME_NAMES, 'Chrome'), 984, 1280)
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0),
                                        functools.partial(QuietHandler, directory=str(lp.ROOT)))
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.br.close()
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=5)

    def test_all_palettes_render_without_layout_errors_and_classics_replay(self):
        br = self.br
        br.cmd('Emulation.setDeviceMetricsOverride',
               {'width': 984, 'height': 1280, 'deviceScaleFactor': 1, 'mobile': False})
        for demo in self.manifest:
            for theme, background in BACKGROUNDS.items():
                with self.subTest(scene=demo['id'], theme=theme):
                    variant = demo['themeVariants'][theme]
                    br.open((OUT / demo['id'] / variant['page']).as_uri() + '?manual')
                    br.seek(3.25)
                    self.assertEqual(br.eval('getComputedStyle(document.getElementById("stage")).backgroundColor'), background)
                    self.assertEqual(br.eval('window.__check()'), [])
                    self.assertEqual(editorial_layout(br), [])
                    self.assertEqual(br.eval('document.querySelectorAll("[data-neon-layer]").length'), len(demo['exportViews']))
                    first = br.shot()
                    br.seek(9.75)
                    self.assertEqual(editorial_layout(br), [])
                    if theme.endswith('-classic'):
                        self.assertGreater(pixel_diff(br, first, br.shot())[0], 24)
                        br.seek(3.25)
                        self.assertEqual(pixel_diff(br, first, br.shot())[0], 0)

    def test_switch_all_four_keeps_time_avatar_and_export_view(self):
        br = self.br
        br.open(f'http://127.0.0.1:{self.server.server_port}/examples/capability-demos/index.html?theme=terminal-classic#rag-explainer')
        self.assertEqual(br.eval('window.galleryState().theme'), 'terminal-classic')
        for demo in self.manifest:
            wait_gallery(br, 'window.selectDemo(' + json.dumps(demo['id']) + ')')
            br.eval('''window.jumpDemo(6.5);document.getElementById('avatar').value='drone';
                document.getElementById('avatar').dispatchEvent(new Event('change'));''')
            view = demo['exportViews'][0]['id']
            br.eval('document.getElementById("exportView").value=' + json.dumps(view))
            for theme in BACKGROUNDS:
                with self.subTest(scene=demo['id'], theme=theme):
                    result = wait_gallery(br, 'document.getElementById("theme").value=' + json.dumps(theme) + ';document.getElementById("theme").dispatchEvent(new Event("change"))')
                    self.assertEqual((result['time'], result['playing'], result['avatar']), (6.5, False, 'drone'))
                    self.assertEqual(br.eval('document.getElementById("exportView").value'), view)
                    self.assertEqual(br.eval('window.__galleryError'), '')
                    path = br.eval('document.getElementById("configLink").getAttribute("href")')
                    self.assertEqual(path, demo['id'] + '/' + demo['themeVariants'][theme]['config'])
                    self.assertEqual(br.eval('document.documentElement.dataset.theme'), theme)

    def test_homepage_has_four_real_media_sets_and_mobile_fits(self):
        br = self.br
        # The showcase is a static site and has no scene readiness flag.
        br.cmd('Page.navigate', {'url': f'http://127.0.0.1:{self.server.server_port}/index.html?theme=pastel-classic'})
        br.eval('''(async()=>{const end=performance.now()+10000;
            while(document.querySelectorAll('[data-scene]').length!==8){
                if(performance.now()>end)throw new Error('showcase readiness timeout');
                await new Promise(resolve=>setTimeout(resolve,30));
            }})()''')
        self.assertEqual(br.eval('document.documentElement.dataset.theme'), 'pastel-classic')
        for theme in BACKGROUNDS:
            br.eval('document.querySelector("[data-theme-choice=' + theme + ']").click()')
            media = br.eval('''Array.from(document.querySelectorAll('[data-scene]')).map(card=>({
                video:card.querySelector('video').getAttribute('src'),poster:card.querySelector('video').getAttribute('poster'),
                download:card.querySelector('.demo-download').href,interactive:card.querySelector('.demo-interactive').href}))''')
            self.assertEqual(len(media), 8)
            for demo, actual in zip(self.manifest, media):
                variant = demo['themeVariants'][theme]
                self.assertTrue(actual['video'].endswith('/' + demo['id'] + '/' + variant['video']))
                self.assertTrue(actual['poster'].endswith('/' + demo['id'] + '/' + variant['poster']))
                self.assertEqual(actual['download'], actual['video'])
                self.assertIn('?theme=' + theme + '#' + demo['id'], actual['interactive'])
                self.assertTrue((OUT / demo['id'] / variant['video']).is_file())
                self.assertTrue((OUT / demo['id'] / variant['poster']).is_file())
        for width in (390, 768, 1280):
            br.cmd('Emulation.setDeviceMetricsOverride', {'width': width, 'height': 900, 'deviceScaleFactor': 1, 'mobile': False})
            self.assertLessEqual(br.eval('document.documentElement.scrollWidth'), width)


if __name__ == '__main__':
    unittest.main()
