"""The two showcase styles keep four palettes and all media links independent."""
import functools
import json
import sys
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import livepanel as lp
from test_four_palette_browser import BACKGROUNDS, QuietHandler


class ShowcaseHandler(QuietHandler):
    def handle(self):
        try:
            super().handle()
        except (BrokenPipeError, ConnectionResetError):
            # Switching a video intentionally aborts the previous HTTP stream.
            pass


class TerminalShowcaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((lp.ROOT / 'examples/capability-demos/manifest.json').read_text(encoding='utf-8'))
        cls.br = lp.Chrome(lp.find_exe(None, lp.CHROME_NAMES, 'Chrome'), 1280, 900)
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(ShowcaseHandler, directory=str(lp.ROOT)))
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.origin = f'http://127.0.0.1:{cls.server.server_port}'

    @classmethod
    def tearDownClass(cls):
        cls.br.close()
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=5)

    def open_home(self, query=''):
        url = self.origin + '/index.html' + query
        if self.br._pw:
            self.br._page.goto(url, wait_until='load')
        else:
            self.br.cmd('Page.navigate', {'url': url})
        self.br.eval('''(async()=>{const end=performance.now()+10000;
            while(document.querySelectorAll('[data-scene]').length!==8||!document.querySelector('#recreation-grid video')){
                if(performance.now()>end)throw new Error('showcase readiness timeout');
                await new Promise(resolve=>setTimeout(resolve,30));
            }await document.fonts.ready;})()''')

    def click_choice(self, kind, value):
        selector = f'[data-{kind}-choice="{value}"]'
        if self.br._pw:
            self.br._page.locator(selector).click()
        else:
            self.br.eval('document.querySelector(' + json.dumps(selector) + ').click()')

    def test_terminal_url_and_both_styles_select_all_eight_matching_media_sets(self):
        self.open_home('?style=terminal&theme=terminal-classic')
        self.assertEqual(self.br.eval('document.documentElement.dataset.style'), 'terminal')
        self.assertEqual(self.br.eval('document.documentElement.dataset.theme'), 'terminal-classic')
        original_fixed_media = self.br.eval('''[...document.querySelectorAll('#recreation-grid video,#export-video')]
            .map(video=>({src:video.src,poster:video.poster}))''')
        for style in ('diagram', 'terminal'):
            self.click_choice('style', style)
            for theme in BACKGROUNDS:
                with self.subTest(style=style, theme=theme):
                    self.click_choice('theme', theme)
                    self.assertEqual(self.br.eval('document.documentElement.dataset.style'), style)
                    self.assertEqual(self.br.eval('document.documentElement.dataset.theme'), theme)
                    self.assertEqual(self.br.eval("document.querySelectorAll('[data-style-choice][aria-pressed=true]').length"), 1)
                    self.assertEqual(self.br.eval("document.querySelectorAll('[data-theme-choice][aria-pressed=true]').length"), 1)
                    media = self.br.eval('''[...document.querySelectorAll('[data-scene]')].map(card=>({
                        id:card.dataset.scene,video:card.querySelector('video').src,poster:card.querySelector('video').poster,
                        download:card.querySelector('.demo-download').href,interactive:card.querySelector('.demo-interactive').href}))''')
                    self.assertEqual(len(media), 8)
                    for demo, actual in zip(self.manifest, media):
                        variant = demo['styleVariants'][style]['themeVariants'][theme]
                        self.assertTrue(actual['video'].endswith('/' + demo['id'] + '/' + variant['video']))
                        self.assertTrue(actual['poster'].endswith('/' + demo['id'] + '/' + variant['poster']))
                        self.assertEqual(actual['download'], actual['video'])
                        parts = urlsplit(actual['interactive'])
                        self.assertEqual(parse_qs(parts.query), {'style': [style], 'theme': [theme]})
                        self.assertEqual(parts.fragment, demo['id'])
                    entry = self.br.eval("document.querySelector('[data-gallery-entry]').href")
                    self.assertEqual(parse_qs(urlsplit(entry).query), {'style': [style], 'theme': [theme]})
                    self.assertEqual(self.br.eval('''[...document.querySelectorAll('#recreation-grid video,#export-video')]
                        .map(video=>({src:video.src,poster:video.poster}))'''), original_fixed_media)

    def test_style_storage_and_url_do_not_overwrite_the_palette_preference(self):
        self.open_home('?style=terminal&theme=light-pastel')
        self.assertEqual(self.br.eval('document.documentElement.dataset.style'), 'terminal')
        self.click_choice('style', 'diagram')
        self.assertEqual(self.br.eval('document.documentElement.dataset.theme'), 'light-pastel')
        self.assertEqual(self.br.eval("localStorage.getItem('motion-diagram-studio-showcase-style')"), 'diagram')
        self.assertEqual(self.br.eval("localStorage.getItem('motion-diagram-studio-showcase-theme')"), 'light-pastel')
        query = parse_qs(urlsplit(self.br.eval('location.href')).query)
        self.assertEqual(query, {'style': ['diagram'], 'theme': ['light-pastel']})
        self.open_home()
        self.assertEqual(self.br.eval('document.documentElement.dataset.style'), 'diagram')
        self.assertEqual(self.br.eval('document.documentElement.dataset.theme'), 'light-pastel')
        self.open_home('?style=terminal&theme=pastel-classic')
        self.assertEqual(self.br.eval('document.documentElement.dataset.style'), 'terminal')
        self.assertEqual(self.br.eval('document.documentElement.dataset.theme'), 'pastel-classic')
        self.open_home('?style=invalid-style&theme=invalid-palette')
        self.assertEqual(self.br.eval('document.documentElement.dataset.style'), 'terminal')
        self.assertEqual(self.br.eval('document.documentElement.dataset.theme'), 'pastel-classic')

    def test_style_and_palette_controls_fit_three_viewport_widths(self):
        for width in (390, 768, 1280):
            if self.br._pw:
                self.br._page.set_viewport_size({'width': width, 'height': 900})
            else:
                self.br.cmd('Emulation.setDeviceMetricsOverride', {'width': width, 'height': 900, 'deviceScaleFactor': 1, 'mobile': False})
            self.open_home('?style=diagram&theme=terminal-dark')
            for style in ('diagram', 'terminal'):
                self.click_choice('style', style)
                for theme, background in BACKGROUNDS.items():
                    with self.subTest(width=width, style=style, theme=theme):
                        self.click_choice('theme', theme)
                        self.assertEqual(self.br.eval('innerWidth'), width)
                        self.assertLessEqual(self.br.eval('document.documentElement.scrollWidth'), width)
                        self.assertEqual(self.br.eval('getComputedStyle(document.body).backgroundColor'), background)
                        self.assertEqual(self.br.eval("document.querySelectorAll('[data-style-choice]').length"), 2)
                        self.assertEqual(self.br.eval("document.querySelectorAll('[data-theme-choice]').length"), 4)


if __name__ == '__main__':
    unittest.main()
