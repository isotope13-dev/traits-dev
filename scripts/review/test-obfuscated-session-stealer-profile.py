#!/usr/bin/env python3
"""Check the obfuscated session-stealer configuration profile."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from zipfile import ZipFile, ZIP_DEFLATED

root = Path(__file__).resolve().parents[2]
cleave = os.environ.get('CLEAVE', str(root.parent / 'cleave/target/release/cleave'))
sample = Path(sys.argv[1])
manifest = (sample / 'package.json').read_text()
script = (sample / 'src/index.js').read_text()
cases = ('positive', 'no-cookie', 'no-seed', 'no-password', 'no-upload', 'no-code', 'short-code')
changes = {'no-cookie': 'cookieSessions', 'no-seed': 'bitcoin-seed',
           'no-password': 'node-passworder', 'no-upload': 'form-data'}
with tempfile.TemporaryDirectory() as directory:
    paths = []
    for case in cases:
        path = Path(directory) / (case + '.zip')
        data = manifest
        if case in changes:
            assert changes[case] in data
            data = data.replace(changes[case], 'redacted')
        with ZipFile(path, 'w', ZIP_DEFLATED) as z:
            z.writestr('package.json', data)
            if case != 'no-code':
                z.writestr('src/index.js', script[:1000] if case == 'short-code' else script)
        paths.append(str(path))
    result = subprocess.run([cleave, '--traits-dir', str(root), '--json', *paths],
                            capture_output=True, text=True, check=True,
                            env={**os.environ, 'CLEAVE_SKIP_CACHE': '1', 'RAYON_NUM_THREADS': '2'})
    rows = [json.loads(line) for line in result.stdout.split('\n') if line]
    assert len(rows) == len(paths)
    for row in rows:
        f = row['files'][0]
        match = any(t['id'].endswith('::obfuscated-session-stealer-profile')
                    for t in f.get('traits', []))
        assert match == f['path'].endswith('/positive.zip'), f['path']
print('Obfuscated session-stealer profile rejects six controls')
