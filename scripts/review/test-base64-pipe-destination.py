#!/usr/bin/env python3
"""Distinguish decoded output written to a named target from a bare pipe."""
from pathlib import Path
import os
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', '../cleave/target/release/cleave')
RULE = 'micro-behaviors/data/decode/to-file::base64-decode-piped-to-file-write'
CASES = [
    ('tee', 'base64 -d | tee output.bin', True),
    ('tee-append', 'base64 -d | tee -a output.bin', True),
    ('tee-append-long', 'base64 -d | tee --append output.bin', True),
    ('dd', 'base64 -d | dd of=output.bin', True),
    ('dd-options', 'base64 -d | dd bs=4096 status=none of=output.bin', True),
    ('bare-tee', 'base64 -d | tee', False),
    ('bare-tee-option', 'base64 -d | tee -a', False),
    ('bare-dd', 'base64 -d | dd bs=4096', False),
]
with tempfile.TemporaryDirectory(prefix='base64-file-probe-') as directory:
    for name, command, expected in CASES:
        target = Path(directory) / (name + '.sh')
        target.write_text('#!/bin/sh\n' + command + '\n# padding\n' * 70)
        result = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), 'test-rules', str(target),
                                 '--rules', RULE], cwd=ROOT, capture_output=True, text=True, check=True)
        prefix = ('MATCHED ' if expected else 'NOT MATCHED ') + RULE + ' '
        assert any(line.startswith(prefix) for line in result.stdout.splitlines()), (name, result.stdout)
        print(name + ': passed', flush=True)
