#!/usr/bin/env python3
"""Encoded scheduled-task paths remain distinct from unrelated hex data."""
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave'))
RULE = 'micro-behaviors/fs/path/config/scheduled::hex-encoded-root-crontab'
with tempfile.TemporaryDirectory(prefix='hex-subject-') as tmp:
    for name, value, expected in (
        ('path.js', '2f6574632f63726f6e746162732f726f6f74', 'MATCHED'),
        ('other.js', '2f6574632f63726f6e746162732f726f6f75', 'NOT MATCHED'),
    ):
        path = Path(tmp) / name
        path.write_text(f"const data = '{value}';\n")
        result = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), 'test-rules', '--rules', RULE, str(path)], text=True, capture_output=True, check=True)
        assert f'{expected} {RULE}' in result.stdout, result.stdout + result.stderr
print('Hex scheduled path: positive and near-miss cases passed')
