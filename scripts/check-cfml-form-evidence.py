#!/usr/bin/env python3
"""Static form declarations must be separated from quoted/commented markup."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

p = argparse.ArgumentParser()
p.add_argument('--cleave', default='cleave')
a = p.parse_args()
root = Path(__file__).resolve().parents[1]
folder = root / 'testdata/taxonomy/cfml-form-evidence'
cases = json.loads((folder / 'cases.json').read_text())
paths = sorted(folder.glob('*.cfm'))
assert {path.stem for path in paths} == set(cases)
original = root / 'testdata/taxonomy/cfml-directory-actions/retained-original.cfm'
assert hashlib.sha256(original.read_bytes()).hexdigest() == '110db2340e0aecb5c59d73b15617b28999d941f974ae04acf4d53ddcf945e9dc'
cases['retained-original'] = {'control': True, 'hostile': True}
paths.append(original)
for path in paths:
    if path.stem == 'datasource-original':
        assert hashlib.sha256(path.read_bytes()).hexdigest() == '987de3c74aaa5371c98365b281fdc3c4b680558aae5b4c9895ec6b8c9fc083d2'
    result = subprocess.run([a.cleave, '--traits-dir', str(root), '--format', 'json', str(path)], capture_output=True, text=True, check=True)
    traits = [t for f in json.loads(result.stdout)['files'] for t in f.get('traits', [])]
    ids = {t['id'] for t in traits}
    expected = cases[path.stem]
    assert ('micro-behaviors/ui/window/form-input::cfml-command-form-field' in ids) == expected['control'], (path.name, ids)
    assert bool([t for t in traits if t['crit'] >= 4]) == expected['hostile'], (path.name, traits)
    if expected['hostile']:
        assert 'micro-behaviors/process/create/exec::cfexecute-request-program' in ids, (path.name, ids)
    print(path.stem + ': passed', flush=True)
