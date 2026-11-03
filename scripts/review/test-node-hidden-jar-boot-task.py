#!/usr/bin/env python3
"""Test independent clues in the elevated boot-task JAR launcher."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
root = Path(__file__).resolve().parents[2]
cleave = os.environ.get('CLEAVE', str(root.parent / 'cleave/target/release/cleave'))
source = Path(sys.argv[1]).read_text()
changes = {
    'no-elevation': ('-Verb RunAs', '-Verb RunAx'),
    'no-task': ('schtasks /create', 'schtasks /query'),
    'no-system': ('/ru "SYSTEM"', '/ru "GUEST"'),
    'no-boot': ('/sc onstart', '/sc onlogon'),
    'no-network-stream': ('res.pipe(stream)', 'res.resume()'),
    'no-extraction': ('extractAllTo', 'extractListx'),
    'no-jar': ("'-jar'", "'-foo'"),
    'no-hidden': ('windowsHide: true', 'windowsHide: false'),
}
with tempfile.TemporaryDirectory() as directory:
    paths = []
    for name in ('positive', *changes):
        data = source
        if name in changes:
            old, new = changes[name]
            assert old in data, name
            data = data.replace(old, new)
        path = Path(directory) / (name + '.js')
        path.write_text(data)
        paths.append(str(path))
    result = subprocess.run([cleave, '--traits-dir', str(root), '--json', *paths],
                            capture_output=True, text=True, check=True,
                            env={**os.environ, 'CLEAVE_SKIP_CACHE': '1'})
    for line in result.stdout.split('\n'):
        if line:
            f = json.loads(line)['files'][0]
            match = any(t['id'].endswith('::node-elevated-boot-task-hidden-jar-stage') for t in f.get('traits', []))
            assert match == f['path'].endswith('/positive.js'), f['path']
print('Boot-task JAR launcher rejects eight missing-evidence controls')
