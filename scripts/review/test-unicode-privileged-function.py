#!/usr/bin/env python3
"""Check the invisible-identifier privileged Function profile."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

root = Path(__file__).resolve().parents[2]
cleave = os.environ.get('CLEAVE', str(root.parent / 'cleave/target/release/cleave'))
source = Path(sys.argv[1]).read_text()
with tempfile.TemporaryDirectory() as directory:
    paths = []
    for name in ('positive', 'no-require', 'no-function', 'no-invisible', 'short-wrapper'):
        data = source
        if name == 'no-require':
            assert 'return require' in data
            data = data.replace('return require', 'return missing')
        elif name == 'no-function':
            assert data.startswith('Function("')
            data = data.replace('Function("', 'Ordinary("')
        elif name == 'no-invisible':
            assert '\\u200C' in data
            data = data.replace('\\u200C', '')
        elif name == 'short-wrapper':
            data = 'Function("x","x")({get"class' + '\\u200C' * 40 + '"(){return require}});'
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
        match = any(t['id'].endswith('::massive-unicode-privileged-function-stage')
                    for t in f.get('traits', []))
        assert match == f['path'].endswith('/positive.js'), f['path']
print('Unicode privileged Function profile rejects four controls')
