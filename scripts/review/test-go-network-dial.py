#!/usr/bin/env python3
"""Go dial classification requires a TCP or UDP network argument."""
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', '../cleave/target/release/cleave')
RULE = 'micro-behaviors/communications/socket/dial::go-dial'
CASES = [('tcp', 'tcp', True), ('udp', 'udp', True), ('unix', 'unix', False)]
with tempfile.TemporaryDirectory(prefix='go-network-dial-') as directory:
    for name, network, expected in CASES:
        target = Path(directory) / (name + '.go')
        target.write_text('package main\nimport "net"\nfunc main() { net.Dial("' + network + '", "localhost:1234") }\n' + '// padding\n' * 60)
        result = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), 'test-rules', str(target),
                                 '--rules', RULE], cwd=ROOT, capture_output=True, text=True, check=True)
        prefix = ('MATCHED ' if expected else 'NOT MATCHED ') + RULE + ' '
        assert any(line.startswith(prefix) for line in result.stdout.splitlines()), (name, result.stdout)
        print(name + ': passed', flush=True)
