"""A terminal presentation remains independent of palette, geometry and timing."""
import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import make_capability_demos as demos


class TerminalConfigurationTests(unittest.TestCase):
    def test_styles_have_distinct_files_for_every_palette(self):
        self.assertEqual(set(demos.STYLE_VARIANTS), {'diagram', 'terminal'})
        for field in ('config', 'page', 'video', 'poster'):
            files = [metadata[field] for style in demos.STYLE_VARIANTS.values()
                     for metadata in style['themeVariants'].values()]
            self.assertEqual(len(files), 8)
            self.assertEqual(len(set(files)), 8)
        self.assertEqual(demos.STYLE_VARIANTS['diagram']['themeVariants'], demos.THEME_VARIANTS)

    def test_terminal_presentation_preserves_source_and_crop_geometry(self):
        for scene in demos.collection():
            before = copy.deepcopy(scene['config'])
            for theme in demos.THEME_VARIANTS:
                with self.subTest(scene=scene['id'], theme=theme):
                    original = demos.theme_config(scene['config'], theme)
                    terminal = demos.presentation_config(original, 'terminal', scene, theme)
                    for field in ('canvas', 'machines', 'elements'):
                        self.assertEqual(terminal[field], original[field])
                    self.assertEqual(terminal['theme'], original['theme'])
                    self.assertEqual(terminal['presentation']['style'], 'terminal')
                    events = terminal['presentation']['events']
                    self.assertEqual(events[0]['t'], 0)
                    self.assertEqual([e['t'] for e in events], sorted(e['t'] for e in events))
                    self.assertTrue(all(0 <= e['t'] < terminal['canvas']['duration'] for e in events))
                    self.assertIn('模拟', events[0]['text'])
                    self.assertIn('config-console-', terminal['presentation']['command'])
            self.assertEqual(scene['config'], before)

    def test_original_style_does_not_add_a_window_or_mutate_the_source(self):
        scene = demos.collection()[0]
        original = demos.theme_config(scene['config'], 'terminal-classic')
        self.assertEqual(demos.presentation_config(original, 'diagram', scene, 'terminal-classic'), original)
        with self.assertRaises(ValueError):
            demos.presentation_config(original, 'unknown', scene, 'terminal-classic')


if __name__ == '__main__':
    unittest.main()
