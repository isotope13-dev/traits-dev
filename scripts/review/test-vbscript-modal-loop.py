#!/usr/bin/env python3
"""Distinguish an unconditional one-statement popup loop from normal prompts."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave'))
RULE = 'objectives/impact/dos/flood::vbs-unbounded-modal-message-loop'
SOURCE = 'Do\n result = MsgBox("Try again", 0, "Prompt")\nLoop\n'
cases = [
    ('unconditional', SOURCE, True),
    ('conditional_start', SOURCE.replace('Do\n', 'Do While running\n'), False),
    ('conditional_end', SOURCE.replace('Loop\n', 'Loop Until done\n'), False),
    ('exit', SOURCE.replace('Loop\n', ' If result = 1 Then Exit Do\nLoop\n'), False),
    ('comment', SOURCE.replace(' result =', " ' result ="), False),
]
with tempfile.TemporaryDirectory() as tmp:
    for name, source, expected in cases:
        path = Path(tmp) / (name + '.vbs')
        path.write_text(source)
        proc = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), '--all-files', '--format=json', str(path)],
                              check=True, capture_output=True, text=True,
                              env={**os.environ, 'CLEAVE_SKIP_CACHE': '1'})
        found = any(t['id'] == RULE for f in json.loads(proc.stdout)['files'] for t in f.get('traits', []))
        assert found == expected, (name, found)
print('VBScript modal loop boundaries passed')
