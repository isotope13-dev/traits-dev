#!/usr/bin/env python3
"""Distinguish complete CFML operation values from their literal fragments."""
import argparse
import json
from pathlib import Path
import subprocess

p = argparse.ArgumentParser()
p.add_argument('--cleave', default='cleave')
a = p.parse_args()
r = Path(__file__).resolve().parents[1]
read = 'micro-behaviors/fs/read/file/full::cffile-read'
post = 'micro-behaviors/communications/http/post::cfhttp-post-request'
cmd = 'micro-behaviors/process/create/shell/request::cfexecute-request-cmd-arguments'
selected = {read, post, cmd}
expected = {name: {read, post} for name in ('literal', 'concatenated', 'interpolated', 'alias', 'alternatives')}
expected.update({name: set() for name in ('constant-fragments', 'interpolated-suffix', 'dynamic-suffix', 'overwritten', 'opaque', 'command-fragments')})
expected['command-concatenated'] = {cmd}
paths = sorted((r / 'testdata/taxonomy/cfml-whole-value').glob('*.cfm'))
assert {path.stem for path in paths} == set(expected)
for path in paths:
    result = subprocess.run([a.cleave, '--traits-dir', str(r), '--format', 'json', str(path)], capture_output=True, text=True, check=True)
    traits = [t for f in json.loads(result.stdout)['files'] for t in f.get('traits', [])]
    assert {t['id'] for t in traits} & selected == expected[path.stem], (path.name, traits)
    if path.stem != 'command-concatenated':
        assert not [t for t in traits if t['crit'] >= 4], (path.name, traits)
    else:
        assert any(t['crit'] == 5 for t in traits), (path.name, traits)
    print(path.stem + ': passed', flush=True)
