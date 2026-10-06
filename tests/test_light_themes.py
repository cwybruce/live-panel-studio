"""Real Chrome acceptance tests for all light scenes and block export metadata.

Run after regenerating the gallery, without needing any external API:
    python -m unittest discover -s tests -p test_light_themes.py -v
"""
import functools
import json
import sys
import threading
import unittest
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import livepanel as lp
from check_frames import pixel_diff, TOL_PIXELS
from verify_capability_demos import platform_fonts, wait_gallery


OUT = lp.ROOT / 'examples/capability-demos'
COUNTS = {'rag-explainer': 5, 'agent-team': 5, 'product-request': 5,
          'knowledge-card': 5, 'business-workflow': 5, 'incident-replay': 4,
          'component-lab': 6, 'avatar-themes': 4}

COLOR_JS = r'''function luminance(color) {
    const m=color.match(/^rgba?\(([^)]+)\)$/);
    if(!m)return null;
    const values=m[1].split(/[ ,/]+/).map(Number);
    if(values.length>3&&values[3]===0)return null;
    const c=values.slice(0,3).map(v=>{v/=255;return v<=.04045?v/12.92:((v+.055)/1.055)**2.4});
    return .2126*c[0]+.7152*c[1]+.0722*c[2];
}'''


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


class LightThemeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads((OUT / 'manifest.json').read_text(encoding='utf-8'))
        cls.br = lp.Chrome(lp.find_exe(None, lp.CHROME_NAMES, 'Chrome'), 984, 1280)
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0),
                                        functools.partial(QuietHandler, directory=str(OUT)))
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.br.close()
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=5)

    def scene(self, scene_id, t=4.5):
        self.br.cmd('Emulation.setDeviceMetricsOverride',
                    {'width': 984, 'height': 1280, 'deviceScaleFactor': 1, 'mobile': False})
        self.br.open((OUT / scene_id / 'live-light.html').as_uri() + '?manual')
        self.br.seek(t)
        self.assertEqual(self.br.eval('window.__error||""'), '')
        return self.br

    def test_all_eight_light_backgrounds_panels_and_title_contrast(self):
        self.assertEqual({d['id'] for d in self.manifest}, set(COUNTS))
        for demo in self.manifest:
            with self.subTest(scene=demo['id']):
                self.assertTrue(demo['themeSwitch'])
                cfg = lp.load_config(OUT / demo['id'] / 'config-light.json')
                self.assertEqual(cfg['theme']['preset'], 'light-pastel')
                self.assertEqual(cfg['theme']['colors']['bg'], '#f1eee5')
                br = self.scene(demo['id'])
                measured = br.eval('''(()=>{''' + COLOR_JS + '''
                    const stage=document.getElementById('stage');
                    const borders=Array.from(stage.querySelectorAll('[data-neon-border]'));
                    const title=Array.from(stage.querySelectorAll('text')).find(n=>
                        Number(n.getAttribute('font-size'))>=28 && /[\u4e00-\u9fff]/.test(n.textContent));
                    const backdrop=stage.querySelector('svg[data-component]:not([data-component="drone"]) > rect');
                    return {
                        body:getComputedStyle(document.body).backgroundColor,
                        stage:getComputedStyle(stage).backgroundColor,
                        backdrop:backdrop&&getComputedStyle(backdrop).fill,
                        panels:borders.map(n=>({id:n.getAttribute('data-neon-border'),
                            fill:getComputedStyle(n).fill,luminance:luminance(getComputedStyle(n).fill)})),
                        title:title&&{text:title.textContent,fill:getComputedStyle(title).fill,
                            luminance:luminance(getComputedStyle(title).fill)},
                        layers:stage.querySelectorAll('[data-neon-layer]').length
                    };
                })()''')
                self.assertEqual(measured['body'], 'rgb(241, 238, 229)')
                self.assertEqual(measured['stage'], 'rgb(241, 238, 229)')
                self.assertEqual(measured['backdrop'], 'rgb(241, 238, 229)')
                self.assertEqual(len(measured['panels']), COUNTS[demo['id']])
                self.assertEqual(measured['layers'], COUNTS[demo['id']])
                for panel in measured['panels']:
                    if panel['fill'] == 'none':
                        continue
                    self.assertIsNotNone(panel['luminance'], panel)
                    self.assertGreaterEqual(panel['luminance'], .08, panel)
                self.assertIsNotNone(measured['title'])
                self.assertIsNotNone(measured['title']['luminance'])
                self.assertLess(measured['title']['luminance'], .35, measured['title'])

    def test_light_layout_fonts_and_exact_replay(self):
        for demo in self.manifest:
            with self.subTest(scene=demo['id']):
                br = self.scene(demo['id'], 3.25)
                for t in (0, 3.25, 6.5, 9.75, 11.9):
                    br.seek(t)
                    self.assertEqual(br.eval('window.__check()'), [])
                fonts = platform_fonts(br)
                self.assertTrue(fonts)
                br.seek(3.25)
                first = br.shot()
                br.seek(9.75)
                br.seek(3.25)
                changed, delta = pixel_diff(br, first, br.shot())
                self.assertEqual(changed, 0, f'replay: {changed} pixels, delta={delta}; tolerance={TOL_PIXELS}')

    def test_gallery_all_themes_visible_and_switch_preserves_state(self):
        br = self.br
        br.cmd('Emulation.setDeviceMetricsOverride',
               {'width': 1440, 'height': 1120, 'deviceScaleFactor': 1, 'mobile': False})
        br.open(f'http://127.0.0.1:{self.server.server_port}/index.html')
        for demo in self.manifest:
            with self.subTest(scene=demo['id']):
                wait_gallery(br, 'document.getElementById("theme").value="terminal-dark";'
                                'window.selectDemo(' + json.dumps(demo['id']) + ')')
                self.assertNotEqual(br.eval('getComputedStyle(document.getElementById("themeLabel")).display'), 'none')
                br.eval('''window.jumpDemo(6.5);
                    const a=document.getElementById('avatar');a.value='drone';
                    a.dispatchEvent(new Event('change'));''')
                before = br.eval('window.galleryState()')
                after = wait_gallery(br, 'document.getElementById("theme").value="light-pastel";'
                                        'document.getElementById("theme").dispatchEvent(new Event("change"))')
                self.assertEqual((after['id'], after['time'], after['playing'], after['avatar']),
                                 (before['id'], 6.5, False, 'drone'))
                self.assertEqual(br.eval('document.documentElement.dataset.theme'), 'light-pastel')
                self.assertEqual(br.eval('document.getElementById("scene").contentWindow.__error||""'), '')
                self.assertTrue(br.eval('''Array.from(document.getElementById('scene').contentDocument
                    .querySelectorAll('[data-avatar=spider]')).every(n=>n.style.display==='none')'''))
                sidebar = br.eval('''(()=>{''' + COLOR_JS + '''
                    return Array.from(document.querySelectorAll('.demo-card'))
                        .map(n=>{for(let p=n;p;p=p.parentElement){
                            const value=luminance(getComputedStyle(p).backgroundColor);
                            if(value!==null)return value;
                        }return null;});})()''')
                self.assertEqual(len(sidebar), 8)
                self.assertTrue(all(v is not None and v >= .08 for v in sidebar), sidebar)

    def test_export_views_cover_every_marked_block_with_safe_even_crop(self):
        for demo in self.manifest:
            with self.subTest(scene=demo['id']):
                br = self.scene(demo['id'])
                sources = br.eval('''(()=>{
                    const stage=document.getElementById('stage'),r=stage.getBoundingClientRect(),
                        sx=r.width/parseFloat(stage.style.width),sy=r.height/parseFloat(stage.style.height);
                    return Array.from(stage.querySelectorAll('[data-neon-border]')).map(n=>{
                        const b=n.getBoundingClientRect();return {id:n.getAttribute('data-neon-border'),
                            x:(b.left-r.left)/sx,y:(b.top-r.top)/sy,w:b.width/sx,h:b.height/sy};});})()''')
                views = demo['exportViews']
                self.assertEqual(len(views), COUNTS[demo['id']])
                self.assertEqual(len({v['id'] for v in views}), len(views))
                self.assertEqual({v['id'] for v in views}, {s['id'] for s in sources})
                by_id = {s['id']: s for s in sources}
                for view in views:
                    self.assertTrue(view['label'].strip(), view)
                    crop = view['crop']
                    self.assertEqual(len(crop), 4)
                    self.assertTrue(all(isinstance(v, int) for v in crop), crop)
                    x, y, w, h = crop
                    self.assertGreater(w, 0)
                    self.assertGreater(h, 0)
                    self.assertEqual(w % 2, 0)
                    self.assertEqual(h % 2, 0)
                    self.assertGreaterEqual(x, 0)
                    self.assertGreaterEqual(y, 0)
                    self.assertLessEqual(x+w, demo['width'])
                    self.assertLessEqual(y+h, demo['height'])
                    source = by_id[view['id']]
                    margins = [source['x']-x, source['y']-y,
                               x+w-source['x']-source['w'], y+h-source['y']-source['h']]
                    for margin in margins:
                        self.assertGreaterEqual(margin, 12-.01, (view, source, margins))
                        self.assertLessEqual(margin, 13.01, (view, source, margins))


if __name__ == '__main__':
    unittest.main()
