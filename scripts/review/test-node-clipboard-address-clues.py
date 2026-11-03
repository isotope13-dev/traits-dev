#!/usr/bin/env python3
"""Check clipboard and address replacement evidence in a reviewed sample."""
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
root = Path(__file__).resolve().parents[2]
cleave = os.environ.get('CLEAVE', str(root.parent / 'cleave/target/release/cleave'))
source = Path(sys.argv[1]).read_text()
changed, count = re.subn(r'(!={1,2})([^;\r\n]{0,500}Set-Clipboard)', r'==\2', source, flags=re.I)
assert count
cases = {
    'positive': source,
    'no-changed-check': changed,
    'no-clipboard-read': source.replace('Get-Clipboard', 'Get-Clipboarx'),
    'no-clipboard-write': source.replace('Set-Clipboard', 'Set-Clipboarx'),
}
with tempfile.TemporaryDirectory() as directory:
    paths = []
    for name, data in cases.items():
        assert name == 'positive' or data != source, name
        path = Path(directory) / (name + '.js')
        path.write_text(data)
        paths.append(str(path))
    result = subprocess.run([cleave, '--traits-dir', str(root), '--json', *paths],
                            capture_output=True, text=True, check=True,
                            env={**os.environ, 'CLEAVE_SKIP_CACHE': '1', 'RAYON_NUM_THREADS': '2'})
    rows = [json.loads(line) for line in result.stdout.split('\n') if line]
    assert len(rows) == len(paths)
    for row in rows:
        f = row['files'][0]
        match = any(t['id'].endswith('::node-cli-clipboard-crypto-clipper') for t in f.get('traits', []))
        assert match == f['path'].endswith('/positive.js'), f['path']
print('Clipboard address rule rejects three missing-evidence controls')
