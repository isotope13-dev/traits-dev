#!/usr/bin/env python3
"""Check real session-existence calls; source snippets alone are insufficient."""
import argparse
import json
from pathlib import Path
import subprocess

p = argparse.ArgumentParser()
p.add_argument('--cleave', default='cleave')
a = p.parse_args()
r = Path(__file__).resolve().parents[1]
positive = {'negative', 'positive', 'elseif', 'constant-name', 'nested-name', 'script'}
negative = {'commented', 'quoted', 'quoted-condition', 'other-scope', 'unknown-name', 'wrong-name', 'sibling-binding'}
paths = sorted((r / 'testdata/taxonomy/cfml-session-evidence').glob('*.cfm'))
assert {path.stem for path in paths} == positive | negative
for path in paths:
    result = subprocess.run([a.cleave, '--traits-dir', str(r), '--format', 'json', str(path)], capture_output=True, text=True, check=True)
    traits = [t for f in json.loads(result.stdout)['files'] for t in f.get('traits', [])]
    ids = {t['id'] for t in traits}
    assert ('micro-behaviors/os/security/auth/session::cfml-session-existence-check' in ids) == (path.stem in positive), (path.name, traits)
    assert 'micro-behaviors/os/security/auth/session::cfml-session-initialization-check' not in ids
    assert not [t for t in traits if t['crit'] >= 4], (path.name, traits)
    print(path.stem + ': passed', flush=True)
