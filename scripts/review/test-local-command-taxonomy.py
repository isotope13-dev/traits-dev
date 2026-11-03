#!/usr/bin/env python3
"""Distinguish shell command targets from starting a shell interpreter."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cleave', default='../cleave/target/release/cleave')
args = parser.parse_args()
with tempfile.TemporaryDirectory(prefix='local-command-taxonomy-') as tmp:
    root = Path(tmp)
    cases = {'direct.sh': './worker', 'shell.sh': 'sh ./worker', 'variable.sh': '"$worker"'}
    for name, command in cases.items():
        (root / name).write_text('#!/bin/sh\n' + command + '\n')
    result = subprocess.run(
        [str((repo / args.cleave).resolve()), '--traits-dir', str(repo), '--format=json',
         *(str(root / name) for name in cases)],
        check=True, capture_output=True, text=True,
    )
    reports = [json.loads(line)['files'][0] for line in result.stdout.splitlines() if line]
    ids = {Path(r['path']).name: {t['id'] for t in r.get('traits', [])} for r in reports}
    assert set(ids) == set(cases), ids.keys()
    assert 'micro-behaviors/process/create/path-execution::execute-dot-slash-literal' in ids['direct.sh']
    assert 'micro-behaviors/process/create/shell/interpreter::sh-local-relative-script' not in ids['direct.sh']
    assert 'micro-behaviors/process/create/shell/interpreter::sh-local-relative-script' in ids['shell.sh']
    assert 'micro-behaviors/process/create/command::execute-quoted-var' in ids['variable.sh']
    print('Direct and variable command targets remain distinct from shell launch.')
