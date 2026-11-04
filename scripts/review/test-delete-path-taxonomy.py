#!/usr/bin/env python3
"""Distinguish unknown filesystem targets from unbound delete-call text."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cleave', default='../cleave/target/release/cleave')
args = parser.parse_args()
with tempfile.TemporaryDirectory(prefix='delete-path-') as tmp:
    root = Path(tmp)
    cases = {
        'remove.js': "const shelljs = require('shelljs'); shelljs.rm('/tmp/example');\n",
        'remove.go': 'package main\nimport "os"\nfunc main() { os.Remove("/tmp/example") }\n',
        'Other.java': 'class Other { void f(Record record) { record.delete(); } }\n',
    }
    for name, content in cases.items():
        (root / name).write_text(content)
    result = subprocess.run(
        [str((repo / args.cleave).resolve()), '--traits-dir', str(repo), '--min-crit', 'baseline',
         '--format=json', *(str(root / name) for name in cases)],
        check=True, capture_output=True, text=True,
    )
    reports = [json.loads(line)['files'][0] for line in result.stdout.splitlines() if line]
    ids = {Path(r['path']).name: {t['id'] for t in r.get('traits', [])} for r in reports}
    assert 'micro-behaviors/fs/delete/path::shelljs-rm' in ids['remove.js'], ids['remove.js']
    assert 'micro-behaviors/fs/delete/path::os-Remove' in ids['remove.go'], ids['remove.go']
    assert 'micro-behaviors/fs/delete/path::zero-argument-delete-call-text' in ids['Other.java'], ids['Other.java']
    assert not any(t.startswith('micro-behaviors/fs/delete/path::') for t in ids['Other.java'])
    print('Path removal and unbound delete-call text remain distinct.')
