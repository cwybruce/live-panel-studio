"""Check real gallery state and source links across display styles and palettes."""
import functools
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import sys
import threading
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import export_demo as ed
import livepanel as lp
from verify_capability_demos import wait_gallery


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


class TerminalGalleryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((ed.DEMO_ROOT / 'manifest.json').read_text(encoding='utf-8'))
        cls.browser = lp.Chrome(lp.find_exe(None, lp.CHROME_NAMES, 'Chrome'), 1280, 1000)
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0),
                                        functools.partial(QuietHandler, directory=str(lp.ROOT)))
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=5)

    def open(self, parameters=''):
        self.browser.open(f'http://127.0.0.1:{self.server.server_port}/examples/capability-demos/index.html'
                          + parameters + '#rag-explainer')

    def change(self, control, value):
        return wait_gallery(self.browser, 'document.getElementById(' + json.dumps(control) + ').value='
                            + json.dumps(value) + ';document.getElementById(' + json.dumps(control)
                            + ').dispatchEvent(new Event("change"))')

    def test_two_avatar_scenes_keep_state_links_and_export_range(self):
        self.open()
        browser = self.browser
        for scene in ('rag-explainer', 'avatar-themes'):
            demo = next(item for item in self.manifest if item['id'] == scene)
            wait_gallery(browser, 'window.selectDemo(' + json.dumps(scene) + ')')
            browser.eval("window.jumpDemo(6.5);document.getElementById('avatar').value='drone';"
                         "document.getElementById('avatar').dispatchEvent(new Event('change'))")
            view = demo['exportViews'][-1]['id']
            browser.eval('document.getElementById("exportView").value=' + json.dumps(view))
            for style in ed.STYLES:
                self.change('style', style)
                for theme in ed.THEMES:
                    with self.subTest(scene=scene, style=style, theme=theme):
                        state = self.change('theme', theme)
                        self.assertEqual((state['id'], state['style'], state['theme'], state['time'],
                                          state['playing'], state['avatar']),
                                         (scene, style, theme, 6.5, False, 'drone'))
                        self.assertEqual(browser.eval('document.getElementById("exportView").value'), view)
                        self.assertEqual(browser.eval('window.__galleryError'), '')
                        self.assertEqual(browser.eval('document.documentElement.dataset.theme'), theme)
                        variant = demo['styleVariants'][style]['themeVariants'][theme]
                        for link, filename in (('configLink', variant['config']), ('htmlLink', variant['page']),
                                                ('videoLink', variant['video'])):
                            self.assertEqual(browser.eval('document.getElementById(' + json.dumps(link)
                                                          + ').getAttribute("href")'), scene + '/' + filename)
                        self.assertEqual(browser.eval('new URL(location.href).searchParams.get("style")'),
                                         None if style == 'diagram' else 'terminal')
                        visible = browser.eval('''(()=>{const doc=document.getElementById('scene').contentDocument,
                            robots=Array.from(doc.querySelectorAll('[data-avatar=drone]')),
                            spiders=Array.from(doc.querySelectorAll('[data-avatar=spider]'));
                            return robots.length>0&&robots.every(node=>node.style.display!=='none')
                                &&spiders.length>0&&spiders.every(node=>node.style.display==='none')})()''')
                        self.assertTrue(visible, 'iframe must display the selected robot, not only retain the control value')

    def test_terminal_url_and_style_switch_keep_playback_running(self):
        self.open('?style=terminal&theme=terminal-classic')
        initial = self.browser.eval('window.galleryState()')
        self.assertEqual((initial['style'], initial['theme']), ('terminal', 'terminal-classic'))
        self.assertTrue(initial['playing'])
        switched = self.change('style', 'diagram')
        self.assertEqual((switched['id'], switched['style'], switched['theme']),
                         ('rag-explainer', 'diagram', 'terminal-classic'))
        self.assertTrue(switched['playing'])

    def test_demo_card_and_reload_preserve_style_and_theme_url(self):
        self.open('?style=terminal&theme=pastel-classic')
        state = wait_gallery(self.browser, 'document.querySelector(\'.demo-card[data-id="agent-team"]\').click()')
        self.assertEqual((state['id'], state['style'], state['theme']),
                         ('agent-team', 'terminal', 'pastel-classic'))
        query = self.browser.eval('''(()=>{const url=new URL(location.href);return {
            style:url.searchParams.get('style'),theme:url.searchParams.get('theme'),hash:url.hash}})()''')
        self.assertEqual(query, {'style': 'terminal', 'theme': 'pastel-classic', 'hash': '#agent-team'})
        self.browser.open(self.browser.eval('location.href'))
        reloaded = self.browser.eval('window.galleryState()')
        self.assertEqual((reloaded['id'], reloaded['style'], reloaded['theme']),
                         ('agent-team', 'terminal', 'pastel-classic'))


if __name__ == '__main__':
    unittest.main()
