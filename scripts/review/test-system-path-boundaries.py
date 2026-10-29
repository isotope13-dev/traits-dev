#!/usr/bin/env python3
"""A public executable path is not an operating-system directory path."""
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', '../cleave/target/release/cleave')
RULE = 'micro-behaviors/fs/path/reference::system-or-library-path-references'
CASES = [
    ('system', 'echo /usr/bin/.example', True),
    ('public', r'echo C:\Users\Public\example.exe', False),
]
with tempfile.TemporaryDirectory(prefix='system-path-boundary-') as directory:
    for name, command, expected in CASES:
        target = Path(directory) / (name + '.sh')
        target.write_text('#!/bin/sh\n' + command + '\n' + '# padding\n' * 60)
        result = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), 'test-rules', str(target),
                                 '--rules', RULE], cwd=ROOT, capture_output=True, text=True, check=True)
        prefix = ('MATCHED ' if expected else 'NOT MATCHED ') + RULE + ' '
        assert any(line.startswith(prefix) for line in result.stdout.splitlines()), (name, result.stdout)
        print(name + ': passed', flush=True)
