#!/usr/bin/env python3
"""Require the Python executable and -c to occupy the actual argv positions."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cleave', default='../cleave/target/release/cleave')
args = parser.parse_args()
with tempfile.TemporaryDirectory(prefix='python-inline-') as tmp:
    root = Path(tmp)
    cases = {
        'positive.py': 'import subprocess\nsubprocess.run(["python3", "-c", code])\n',
        'wrong_executable.py': 'import subprocess\nsubprocess.run(["echo", "python3", "-c"])\n',
        'wrong_option.py': 'import subprocess\nsubprocess.run(["python3", "-m", "-c"])\n',
    }
    for name, source in cases.items():
        (root / name).write_text(source)
    result = subprocess.run(
        [str((repo / args.cleave).resolve()), '--traits-dir', str(repo), '--min-crit', 'component',
         '--format=json', *(str(root / name) for name in cases)],
        check=True, capture_output=True, text=True,
    )
    reports = [json.loads(line)['files'][0] for line in result.stdout.splitlines() if line]
    ids = {Path(r['path']).name: {t['id'] for t in r.get('traits', [])} for r in reports}
    expected = {'micro-behaviors/process/deploy/interpreter-command::python-c-flag',
                'micro-behaviors/process/deploy/interpreter-command::python3-inline-command'}
    assert set(ids) == set(cases), ids.keys()
    assert expected <= ids['positive.py'], ids['positive.py']
    for name in ('wrong_executable.py', 'wrong_option.py'):
        assert not expected & ids[name], (name, ids[name])
    print('Python inline launch requires the executable and -c in the first two positions.')
