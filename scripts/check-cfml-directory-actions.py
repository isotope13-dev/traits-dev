#!/usr/bin/env python3
"""Check parsed directory actions and unquoted attribute semantics; never execute CFML."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
ids = {
    'create': 'micro-behaviors/fs/directory/mkdir::cfdirectory-create',
    'delete': 'micro-behaviors/fs/delete/directory::cfdirectory-delete',
    'list': 'micro-behaviors/fs/directory/readdir::cfdirectory-list',
}
expected = {name: set() for name in ['bare-alias', 'overwritten', 'commented', 'quoted', 'prefix', 'suffix', 'duplicate', 'wrong-call', 'bare-request', 'bare-request-alias', 'interpolated-request', 'unquoted-shell']}
for name in ['create', 'unquoted-create']: expected[name] = {ids['create']}
for name in ['delete', 'unquoted-delete', 'alias', 'shadowed-literal', 'concatenated', 'interpolated']: expected[name] = {ids['delete']}
for name in ['list', 'wrong-field']: expected[name] = {ids['list']}
expected['retained-original'] = {ids['create'], ids['list']}
paths = sorted((root / 'testdata/taxonomy/cfml-directory-actions').glob('*.cfm'))
assert {p.stem for p in paths} == set(expected)
for path in paths:
    if path.stem == 'retained-original':
        assert hashlib.sha256(path.read_bytes()).hexdigest() == '110db2340e0aecb5c59d73b15617b28999d941f974ae04acf4d53ddcf945e9dc'
    result = subprocess.run([args.cleave, '--traits-dir', str(root), '--format', 'json', str(path)], capture_output=True, text=True, check=True)
    traits = [t for f in json.loads(result.stdout)['files'] for t in f.get('traits', [])]
    found = {t['id'] for t in traits}
    assert found & set(ids.values()) == expected[path.stem], (path.name, found)
    hostile = [t for t in traits if t['crit'] >= 4]
    assert bool(hostile) == (path.stem in ['interpolated-request', 'unquoted-shell', 'retained-original']), (path.name, hostile)
    assert ('micro-behaviors/process/create/exec::cfexecute-request-program' in found) == (path.stem in ['interpolated-request', 'retained-original']), (path.name, found)
    print(path.stem + ': passed', flush=True)
