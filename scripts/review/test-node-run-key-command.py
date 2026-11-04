#!/usr/bin/env python3
"""Recognize Node reg-add argv without confusing queries or unrelated keys."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
source = r'''const cp = require('child_process');
cp.spawn('reg', ['add', 'HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run', '/v', name, '/t', 'REG_SZ', '/d', cmd, '/f']);
'''
cases = {'write.js': source, 'query.js': source.replace("'add'", "'query'"),
         'other-key.js': source.replace('CurrentVersion\\\\Run', 'CurrentVersion\\\\Explorer'),
         'no-data.js': source.replace("'/d'", "'/v'"),
         'other-command.js': source.replace("'reg'", "'echo'")}
with tempfile.TemporaryDirectory(prefix='node-run-key-') as temp:
    root = Path(temp)
    for name, body in cases.items():
        (root / name).write_text(body)
    p = subprocess.run([args.cleave, '--traits-dir', str(repo), '--min-crit', 'component',
                        '--format=json', *(str(root / n) for n in cases)],
                       check=True, capture_output=True, text=True)
    found = {Path(f['path']).name: {t['id'] for t in f.get('traits', [])}
             for line in p.stdout.splitlines() if line for f in json.loads(line)['files']}
    trait = 'micro-behaviors/os/registry/autostart/write::node-reg-add-run-value'
    assert trait in found['write.js']
    assert all(trait not in found[n] for n in cases if n != 'write.js')
    print('Node Run-key write requires reg add, Run key and value data.')
