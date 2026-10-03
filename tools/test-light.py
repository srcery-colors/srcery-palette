#!/usr/bin/env python3
"""Check WCAG references, canonical provenance, and candidate reproducibility."""
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('light', ROOT / 'tools/generate-light.py')
light = importlib.util.module_from_spec(spec)
spec.loader.exec_module(light)


class LightPaletteTests(unittest.TestCase):
    def test_wcag_reference_values_and_threshold(self):
        self.assertEqual(light.contrast('#000000', '#FFFFFF'), 21)
        self.assertEqual(light.contrast('#FFFFFF', '#FFFFFF'), 1)
        self.assertAlmostEqual(light.contrast('#00FF00', '#000000'), 15.304, places=3)
        self.assertLess(light.contrast('#777777', '#FFFFFF'), 4.5)
        self.assertGreater(light.contrast('#767676', '#FFFFFF'), 4.5)

    def test_candidate_is_reproducible_from_canonical(self):
        canonical = json.loads((ROOT / 'palette.json').read_text())
        expected = json.loads((ROOT / 'palette-light.json').read_text())
        self.assertEqual(light.generate_palette(canonical, 4.5, fix_cterm=True), expected)
        vim = ROOT.parent / 'srcery-vim'
        if vim.exists():
            self.assertEqual(light.generate_vim((vim / 'colors/srcery.vim').read_text(), expected, True),
                             (vim / 'colors/srcery-light.vim').read_text())
            self.assertEqual(expected, json.loads((vim / 'tests/light-palette.json').read_text()))

    def test_audit_and_accent_hue_constraints(self):
        result = json.loads((ROOT / 'light/iterations/02/contrast.json').read_text())
        self.assertEqual({p['editor'] for p in result['pairs']}, {'vim', 'nvim'})
        self.assertEqual({p['mode'] for p in result['pairs']}, {'gui', 'cterm'})
        self.assertEqual(result['failures'], [])
        for pair in result['pairs']:
            self.assertGreaterEqual(pair['ratio'], pair['target'], str(pair))
        canonical = json.loads((ROOT / 'palette.json').read_text())
        palette = json.loads((ROOT / 'palette-light.json').read_text())
        for name in ('red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'orange',
                     'bright_orange', 'bright_red', 'bright_green', 'bright_yellow',
                     'bright_blue', 'bright_magenta', 'bright_cyan', 'teal'):
            h0 = light.hls(canonical[name]['hex'])[0]
            h1 = light.hls(palette[name]['hex'])[0]
            self.assertLess(abs(((h1 - h0) * 360 + 180) % 360 - 180), 1, name)


if __name__ == '__main__':
    unittest.main()
