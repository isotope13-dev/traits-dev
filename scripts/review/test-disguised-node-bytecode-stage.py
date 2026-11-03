#!/usr/bin/env python3
"""Check the disguised native and bytecode launcher across archive members."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from zipfile import ZipFile

root = Path(__file__).resolve().parents[2]
cleave = os.environ.get('CLEAVE', str(root.parent / 'cleave/target/release/cleave'))
sample = Path(sys.argv[1])
script = (sample / 'CHANGELOG.md').read_bytes()
dll = (sample / 'python314.dll').read_bytes()
addon = (sample / 'default.node').read_bytes()
cases = ('positive', 'no-proxy', 'no-changelog-name', 'no-asar',
         'no-bytecode', 'no-bytenode', 'no-native-addon', 'plain-script')
with tempfile.TemporaryDirectory() as directory:
    paths = []
    for case in cases:
        path = Path(directory) / (case + '.zip')
        js = script
        if case in ('no-asar', 'no-bytecode', 'no-bytenode'):
            before = {'no-asar': b'./app.asar', 'no-bytecode': b'app.jsc',
                      'no-bytenode': b'bytenode'}[case]
            assert before in js
            js = js.replace(before, b'X' * len(before))
        elif case == 'plain-script':
            js = b'./app.asar extractAll app.jsc bytenode'
        with ZipFile(path, 'w') as z:
            if case != 'no-proxy':
                z.writestr('python314.dll', dll)
            if case != 'no-native-addon':
                z.writestr('resources/default.node', addon)
            name = 'resources/readme.js' if case == 'no-changelog-name' else 'resources/CHANGELOG.md'
            z.writestr(name, js)
        paths.append(str(path))
    result = subprocess.run([cleave, '--traits-dir', str(root), '--json', *paths],
                            capture_output=True, text=True, check=True,
                            env={**os.environ, 'CLEAVE_SKIP_CACHE': '1', 'RAYON_NUM_THREADS': '2'})
    rows = [json.loads(line) for line in result.stdout.split('\n') if line]
    assert len(rows) == len(paths)
    for row in rows:
        f = row['files'][0]
        match = any(t['id'].endswith('::disguised-python-node-bytecode-chain')
                    for t in f.get('traits', []))
        assert match == f['path'].endswith('/positive.zip'), f['path']
print('Disguised bytecode chain rejects seven controls')
