#!/usr/bin/env python3
"""CFML tags after script blocks remain visible; script strings stay opaque."""
import argparse
import json
from pathlib import Path
import subprocess

p = argparse.ArgumentParser()
p.add_argument('--cleave', default='cleave')
a = p.parse_args()
r = Path(__file__).resolve().parents[1]
positive = {'after-script', 'multiple-blocks'}
expected = positive | {'quoted-closing', 'comment-closing', 'unterminated', 'stale-alias'}
paths = sorted((r / 'testdata/taxonomy/cfml-script-boundary').glob('*.cfm'))
assert {path.stem for path in paths} == expected
for path in paths:
    result = subprocess.run([a.cleave, '--traits-dir', str(r), '--format', 'json', str(path)], capture_output=True, text=True, check=True)
    traits = [t for f in json.loads(result.stdout)['files'] for t in f.get('traits', [])]
    ids = {t['id'] for t in traits}
    assert ('objectives/command-and-control/backdoor/webshell/request::cfml-request-command-shell' in ids) == (path.stem in positive), (path.name, traits)
    assert ('micro-behaviors/process/create/exec::cfexecute-tag' in ids) == (path.stem in positive | {'stale-alias'}), (path.name, traits)
    if path.stem not in positive:
        assert not [t for t in traits if t['crit'] >= 4], (path.name, traits)
    print(path.stem + ': passed', flush=True)
