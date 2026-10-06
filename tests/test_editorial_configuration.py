"""Real-browser checks that editing public JSON changes the authored scene."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import livepanel as lp


class EditorialConfigTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory(prefix='livepanel-config-')
        cls.br = lp.Chrome(lp.find_exe(None, lp.CHROME_NAMES, 'Chrome'), 984, 1280)

    @classmethod
    def tearDownClass(cls):
        cls.br.close()
        cls.tmp.cleanup()

    def scene(self, name, edit, t):
        cfg = lp.load_config(lp.ROOT / 'examples/capability-demos' / name / 'config.json')
        edit(cfg)
        path = Path(self.tmp.name) / 'config.json'
        path.write_text(json.dumps(cfg, ensure_ascii=False), encoding='utf-8')
        page = Path(self.tmp.name) / 'live.html'
        lp.build_page(path, page)
        self.br.open(page.as_uri() + '?manual')
        self.br.seek(t)
        self.assertEqual(self.br.eval('window.__error||""'), '')
        return self.br

    def test_rag_period_drives_active_step(self):
        br = self.scene('rag-explainer', lambda c: c['machines']['rag'].update(period=2), 4.5)
        self.assertEqual(br.eval('document.querySelector("[data-step=\\"2\\"]").getAttribute("opacity")'), '1')
        self.assertIn('筛选证据', br.eval('document.querySelector("[data-stage-label]").textContent'))
        self.assertEqual(br.eval('document.querySelector("[data-component=drone] > rect").getAttribute("x")'), '547')

    def test_knowledge_period_and_counter_follow_json(self):
        def edit(c):
            c['machines']['chapter']['period'] = 2
            c['machines']['views'].update(start=900, rate=0)
        br = self.scene('knowledge-card', edit, 4.5)
        self.assertIn('检查输出', br.eval('document.querySelector("[data-chapter-label]").textContent'))
        self.assertIn('900', br.eval('document.querySelector("[data-view-count]").textContent'))
        self.assertEqual(br.eval('document.querySelector("[data-component=drone] > rect").getAttribute("x")'), '687')

    def test_workflow_counter_and_review_follow_json(self):
        def edit(c):
            c['machines']['received'].update(start=80, rate=3)
            c['machines']['review'].update(period=10, run=9)
        br = self.scene('business-workflow', edit, 5)
        self.assertIn('95', br.eval('document.querySelector("[data-received]").textContent'))
        self.assertIn('复核处理中', br.eval('document.querySelector("[data-review-label]").textContent'))

    def test_avatar_cycle_period_drives_focus_label(self):
        br = self.scene('avatar-themes', lambda c: c['machines']['guide'].update(period=2), 4.5)
        self.assertIn('解释结果', br.eval('document.querySelector("[data-current-label]").textContent'))


if __name__ == '__main__':
    unittest.main()
