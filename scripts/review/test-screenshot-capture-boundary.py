#!/usr/bin/env python3
"""A screen-capture library constructor is not a screenshot."""
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', '../cleave/target/release/cleave')
RULE = 'micro-behaviors/hardware/display/screenshot::screen-capture'
CASES = [
    ('constructor', 'import mss\nsct = mss.mss()', False),
    ('capture', 'import pyautogui\nimage = pyautogui.screenshot()', True),
]
with tempfile.TemporaryDirectory(prefix='screen-capture-boundary-') as directory:
    for name, code, expected in CASES:
        target = Path(directory) / (name + '.py')
        target.write_text(code + '\n' + '# padding\n' * 60)
        result = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), 'test-rules', str(target),
                                 '--rules', RULE], cwd=ROOT, capture_output=True, text=True, check=True)
        prefix = ('MATCHED ' if expected else 'NOT MATCHED ') + RULE + ' '
        assert any(line.startswith(prefix) for line in result.stdout.splitlines()), (name, result.stdout)
        print(name + ': passed', flush=True)
