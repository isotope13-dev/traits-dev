#!/usr/bin/env python3
"""Distinguish file-backed curl bodies from stdin and non-HTTP destinations."""
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', '../cleave/target/release/cleave')
RULE = 'micro-behaviors/communications/http/upload/file::curl-explicit-file-http-body'
CASES = [
    ('file', 'curl --data-binary @/tmp/report.txt https://example.com/upload', True),
    ('stdin', 'curl --data-binary @- https://example.com/upload', False),
    ('ftp', 'curl --data-binary @/tmp/report.txt ftp://example.com/upload', False),
]
with tempfile.TemporaryDirectory(prefix='curl-file-body-') as directory:
    for name, command, expected in CASES:
        target = Path(directory) / (name + '.sh')
        target.write_text('#!/bin/sh\n' + command + '\n' + '# padding\n' * 60)
        result = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), 'test-rules', str(target),
                                 '--rules', RULE], cwd=ROOT, capture_output=True, text=True, check=True)
        prefix = ('MATCHED ' if expected else 'NOT MATCHED ') + RULE + ' '
        assert any(line.startswith(prefix) for line in result.stdout.splitlines()), (name, result.stdout)
        print(name + ': passed', flush=True)
