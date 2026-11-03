#!/usr/bin/env python3
"""Check the shuffled wallet and browser upload profile."""
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
    'no-wallet-prefix': ('nkbih', 'nkbix'),
    'no-wallet-middle': ('fbeog', 'fbeox'),
    'no-wallet-suffix': ('fgpgk', 'fgpgx'),
    'no-login': ('/Logi', '/Logx'),
    'no-upload': ('/uplo', '/uplx'),
    'no-form': ('formD', 'formX'),
    'no-stream': ('Strea', 'Strex'),
    'no-fs': ("require('fs')", "require('xx')"),
    'no-os': ("require('os')", "require('xx')"),
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
                            env={**os.environ, 'CLEAVE_SKIP_CACHE': '1', 'RAYON_NUM_THREADS': '2'})
    rows = [json.loads(line) for line in result.stdout.split('\n') if line]
    assert len(rows) == len(paths)
    for row in rows:
        f = row['files'][0]
        match = any(t['id'].endswith('::obfuscated-wallet-login-upload-clues') for t in f.get('traits', []))
        assert match == f['path'].endswith('/positive.js'), f['path']
print('Obfuscated wallet and login profile rejects nine controls')
