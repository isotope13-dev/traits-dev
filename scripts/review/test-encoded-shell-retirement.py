#!/usr/bin/env python3
"""Decoded shell input remains distinct from decoded data sent elsewhere."""
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave'))
RULE = 'micro-behaviors/process/deploy/interpreter-stdin/decoded::literal-base64-decoded-shell-pipeline'
blob = 'QUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFB'
with tempfile.TemporaryDirectory(prefix='encoded-shell-') as tmp:
    for name, sink, expected in [('shell.sh', 'sh', 'MATCHED'), ('data.sh', 'cat', 'NOT MATCHED')]:
        path = Path(tmp) / name
        path.write_text(f"printf '%s' '{blob}' | base64 -d | {sink}\n")
        result = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), 'test-rules', '--rules', RULE, str(path)], text=True, capture_output=True, check=True)
        assert f'{expected} {RULE}' in result.stdout, result.stdout + result.stderr
print('Decoded interpreter stdin: shell and data-sink cases passed')
