# /// script
# dependencies = ["pyyaml"]
# ///
"""Compatibility entry point for the recorded loop-neighborhood audit."""
from pathlib import Path
import runpy
import sys

script = Path(__file__).with_name('check-taxonomy-move-preservation.py')
sys.argv = [str(script), 'control-flow']
runpy.run_path(str(script), run_name='__main__')
