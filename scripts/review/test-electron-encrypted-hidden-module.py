#!/usr/bin/env python3
"""Exercise the archive-level hidden encrypted JavaScript stage."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from zipfile import ZipFile, ZIP_DEFLATED
root = Path(__file__).resolve().parents[2]
cleave = os.environ.get('CLEAVE', str(root.parent / 'cleave/target/release/cleave'))
loader = Path(sys.argv[1]).read_text()
payload = Path(sys.argv[2]).read_text()
changes = {
    'no-prefix-check': ('.startsWith(', '.startsWitx('),
    'no-suffix-check': ('.endsWith(', '.endsWitx('),
    'no-xor': ('encryptedBuffer[i] ^ key[i % key.length]', 'encryptedBuffer[i] | key[i % key.length]'),
    'no-require-parameter': ("new Function('require'", "new Function('sandbox'"),
    'no-file-read': ('fs.readFileSync', 'fs.statSync'),
    'no-hidden-window': ('width: 1, height: 1', 'width: 500, height: 500'),
    'no-delay': ('setTimeout(', 'setImmediate('),
}
with tempfile.TemporaryDirectory() as directory:
    paths = []
    for name in ('positive', *changes, 'no-encoded-marker', 'low-entropy'):
        l, p = loader, payload
        if name in changes:
            old, new = changes[name]
            assert old in l, name
            l = l.replace(old, new)
        elif name == 'no-encoded-marker':
            assert p.startswith('__ENC__')
            p = 'ordinary' + p[7:]
        elif name == 'low-entropy':
            p = '__ENC__' + 'A' * (len(p) - 14) + '__ENC__'
        path = Path(directory) / (name + '.zip')
        with ZipFile(path, 'w', ZIP_DEFLATED) as z:
            z.writestr('app.js', l)
            z.writestr('src/module.js', p)
        paths.append(str(path))
    result = subprocess.run([cleave, '--traits-dir', str(root), '--json', *paths],
                            capture_output=True, text=True, check=True,
                            env={**os.environ, 'CLEAVE_SKIP_CACHE': '1', 'RAYON_NUM_THREADS': '2'})
    rows = [json.loads(line) for line in result.stdout.split('\n') if line]
    assert len(rows) == len(paths)
    for row in rows:
        f = row['files'][0]
        match = any(t['id'].endswith('::archive-hidden-xor-source-stage') for t in f.get('traits', []))
        assert match == f['path'].endswith('/positive.zip'), f['path']
print('Hidden encrypted source stage rejects nine missing-evidence controls')
