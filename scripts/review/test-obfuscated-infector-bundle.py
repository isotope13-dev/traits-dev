#!/usr/bin/env python3
"""Check that every bundled capability and obfuscation clue is required."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

root = Path(__file__).resolve().parents[2]
cleave = os.environ.get('CLEAVE', str(root.parent / 'cleave/target/release/cleave'))
source = Path(sys.argv[1]).read_text()
names = ('usb_infector', 'clipper', 'phish', 'uploadFiles', 'persist', 'injection')
with tempfile.TemporaryDirectory() as directory:
    paths = []
    for name in ('positive', *names, 'unobfuscated'):
        data = source
        if name in names:
            before = 'utils/' + name + '.js'
            assert before in data
            data = data.replace(before, 'utils/redacted.js')
        elif name == 'unobfuscated':
            data = ''.join("'utils/" + n + ".js':[function(){}],\n" for n in names)
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
        match = any(t['id'].endswith('::obfuscated-infector-clipper-phish-bundle')
                    for t in f.get('traits', []))
        assert match == f['path'].endswith('/positive.js'), f['path']
print('Obfuscated infector bundle rejects seven controls')
