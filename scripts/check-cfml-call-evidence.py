#!/usr/bin/env python3
"""Static CFML call/argument evidence; never execute fixture source."""
import argparse
import json
from pathlib import Path
import subprocess

p = argparse.ArgumentParser()
p.add_argument('--cleave', default='cleave')
a = p.parse_args()
r = Path(__file__).resolve().parents[1]
selected = {
    'micro-behaviors/crypto/symmetric/encrypt::cfml-encrypted-request-url',
    'micro-behaviors/communications/http/post::cfhttp-post-request',
    'micro-behaviors/fs/directory/readdir::cfdirectory-list',
}
expected = {name: set() for name in (
    'wrong-argument', 'wrong-operation', 'wrong-field', 'quoted', 'commented', 'overwritten'
)}
expected['direct'] = selected
expected['alias'] = {'micro-behaviors/crypto/symmetric/encrypt::cfml-encrypted-request-url'}
paths = sorted((r / 'testdata/taxonomy/cfml-call-evidence').glob('*.cfm'))
assert {path.stem for path in paths} == set(expected)
for path in paths:
    result = subprocess.run(
        [a.cleave, '--traits-dir', str(r), '--format', 'json', str(path)],
        capture_output=True, text=True, check=True,
    )
    traits = [t for f in json.loads(result.stdout)['files'] for t in f.get('traits', [])]
    ids = {t['id'] for t in traits}
    assert ids & selected == expected[path.stem], (path.name, traits)
    assert 'micro-behaviors/fs/directory/readdir::cfdirectory-query-list' not in ids
    assert not [t for t in traits if t['crit'] >= 4], (path.name, traits)
    print(path.stem + ': passed', flush=True)
