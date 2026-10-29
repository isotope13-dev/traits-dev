#!/usr/bin/env python3
"""A descriptor write must not be classified as a whole-file write."""
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', '../cleave/target/release/cleave')
FILE = 'micro-behaviors/fs/write/file/full/unspecified::write-file-sync'
DESCRIPTOR = 'micro-behaviors/data/stream/write::node-write-sync-buffer'
CASES = [
    ('file', 'fs.writeFileSync("out.txt", "hello");', True, False),
    ('descriptor', 'fs.writeSync(1, "hello");', False, True),
]
with tempfile.TemporaryDirectory(prefix='node-write-boundary-') as directory:
    for name, command, expected_file, expected_descriptor in CASES:
        target = Path(directory) / (name + '.js')
        target.write_text('const fs = require("fs");\n' + command + '\n' + '// padding\n' * 60)
        result = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), 'test-rules', str(target),
                                 '--rules', FILE + ',' + DESCRIPTOR], cwd=ROOT,
                                capture_output=True, text=True, check=True)
        for rule, expected in ((FILE, expected_file), (DESCRIPTOR, expected_descriptor)):
            prefix = ('MATCHED ' if expected else 'NOT MATCHED ') + rule + ' '
            assert any(line.startswith(prefix) for line in result.stdout.splitlines()), (name, result.stdout)
        print(name + ': passed', flush=True)
