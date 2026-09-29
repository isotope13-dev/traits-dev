#!/usr/bin/env python3
"""Check parsed CFEXECUTE calls and output-file attributes, without execution."""
import argparse
import json
from pathlib import Path
import subprocess

p = argparse.ArgumentParser()
p.add_argument('--cleave', default='cleave')
a = p.parse_args()
r = Path(__file__).resolve().parents[1]
call = 'micro-behaviors/process/create/exec::cfexecute-tag'
output = 'micro-behaviors/process/create/exec::cfexecute-output-file'
expected = {name: {call, output} for name in ('literal', 'dynamic', 'opaque')}
expected.update({name: {call} for name in ('missing', 'wrong-attribute')})
expected.update({name: set() for name in ('commented', 'quoted', 'wrong-call', 'duplicate', 'function-name')})
paths = sorted((r / 'testdata/taxonomy/cfml-execute-evidence').glob('*.cfm'))
assert {path.stem for path in paths} == set(expected)
for path in paths:
    result = subprocess.run([a.cleave, '--traits-dir', str(r), '--format', 'json', str(path)], capture_output=True, text=True, check=True)
    traits = [t for f in json.loads(result.stdout)['files'] for t in f.get('traits', [])]
    assert {t['id'] for t in traits} & {call, output} == expected[path.stem], (path.name, traits)
    assert not [t for t in traits if t['crit'] >= 4], (path.name, traits)
    print(path.stem + ': passed', flush=True)
