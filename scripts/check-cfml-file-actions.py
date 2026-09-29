#!/usr/bin/env python3
"""Verify CFML file action routing without executing the source fixtures."""
import argparse
import json
from pathlib import Path
import subprocess

p = argparse.ArgumentParser()
p.add_argument('--cleave', default='cleave')
a = p.parse_args()
r = Path(__file__).resolve().parents[1]
actions = {
    'read': 'micro-behaviors/fs/read/file/full::cffile-read',
    'write': 'micro-behaviors/fs/write/content::cffile-write',
    'upload': 'micro-behaviors/fs/write/content::cffile-upload',
    'delete': 'micro-behaviors/fs/delete/file/command::cffile-delete',
    'move': 'micro-behaviors/fs/file/move::cffile-move',
    'copy': 'micro-behaviors/fs/file/copy::cffile-copy',
}
expected = {k: {v} for k, v in actions.items()}
expected.update({alias: {actions[key]} for alias, key in (
    ('readbinary', 'read'), ('append', 'write'), ('uploadall', 'upload'), ('rename', 'move')
)})
expected.update({name: set() for name in ('commented', 'quoted', 'prefixes', 'wrong-field')})
selected = set(actions.values()) | {'micro-behaviors/fs/file/read-write::cfml-multiple-file-operations'}
paths = sorted((r / 'testdata/taxonomy/cfml-file-actions').glob('*.cfm'))
assert {path.stem for path in paths} == set(expected)
for path in paths:
    result = subprocess.run(
        [a.cleave, '--traits-dir', str(r), '--format', 'json', str(path)],
        capture_output=True, text=True, check=True,
    )
    traits = [t for f in json.loads(result.stdout)['files'] for t in f.get('traits', [])]
    ids = {t['id'] for t in traits}
    assert ids & selected == expected[path.stem], (path.name, traits)
    assert 'micro-behaviors/fs/file/move::cffile-relocate' not in ids
    assert not [t for t in traits if t['crit'] >= 4], (path.name, traits)
    print(path.stem + ': passed', flush=True)
