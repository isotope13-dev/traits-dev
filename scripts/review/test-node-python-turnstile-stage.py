#!/usr/bin/env python3
"""Check the detached network-fed Python staging clues."""
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
    'no-runtime-download': ('https://www.python.org/ftp/python/3.12.8/python-3.12.8-embed-amd64.zip', 'https://example.invalid/assets/archive.zip'),
    'no-extraction': ('Expand-Archive', 'Expand-Archived'),
    'no-pythonw': ('pythonw.exe', 'program.exe'),
    'no-network-response': ('https.get(', 'https.noop('),
    'no-stdin-write': ('.stdin.write(', '.stdin.noop('),
    'no-detached-handle': ('.unref()', '.ref()'),
    'no-turnstile': ('turnstile', 'othergate'),
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
    rows = [json.loads(line) for line in result.stdout.split('\n') if line]
    assert len(rows) == len(paths)
    for row in rows:
        f = row['files'][0]
        match = any(t['id'].endswith('::node-detached-python-remote-stage-turnstile') for t in f.get('traits', []))
        assert match == f['path'].endswith('/positive.js'), f['path']
print('Detached Python staging rule rejects seven missing-evidence controls')
