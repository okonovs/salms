"""Guard the generated graph's grayscale routing against regressions."""
from pathlib import Path
import re
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]

class GraphTests(unittest.TestCase):
    def test_grayscale_is_exterior_only(self):
        subprocess.run([sys.executable, str(ROOT/'scripts/build_release.py')], check=True, capture_output=True)
        graph = (ROOT/'dist/Salms Random Window.setting').read_text()
        def inputs(node):
            return re.search(r'\b'+node+r' = \w+ \{\s*Inputs = \{(.*?)\n   \},', graph, re.S).group(1)
        self.assertIn('SourceOp = "SalmsFilmGrain"', inputs('SalmsGrayscale'))
        self.assertIn('Saturation = Input { Expression = "1-SalmsRectangle.Grayscale" }', inputs('SalmsGrayscale'))
        sharp = inputs('SalmsSharpWindow')
        self.assertIn('Background = Input { SourceOp = "SalmsGrayscale"', sharp)
        self.assertIn('Foreground = Input { SourceOp = "SalmsTimeline"', sharp)
        border = inputs('SalmsBorder')
        self.assertIn('Background = Input { SourceOp = "SalmsSharpWindow"', border)
        self.assertIn('Foreground = Input { SourceOp = "SalmsWhite"', border)
