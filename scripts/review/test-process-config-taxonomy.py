#!/usr/bin/env python3
"""Keep process construction and input references in their evidence homes."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cleave', default='../cleave/target/release/cleave')
args = parser.parse_args()
with tempfile.TemporaryDirectory(prefix='process-config-') as tmp:
    root = Path(tmp)
    cases = {
        'task.go': 'package main\nimport "os/exec"\nfunc x() { exec.Command("node", "-e", task.Code) }\n',
        'argv.py': 'args = ["node", "-e", code]\n',
        'forward.js': 'handlers["run"](spawn, target, ["-e", source], {});\n',
        'negative.py': 'args = ["node", "-p", code]\n',
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
    expected = {
        'task.go': 'micro-behaviors/process/create/subprocess/configure::go-node-eval-task-field',
        'argv.py': 'metadata/file/profile/execution-api::python-argv-node-eval',
        'forward.js': 'metadata/file/profile/execution-api::js-helper-receives-spawn-inline-source',
    }
    assert set(ids) == set(cases), ids.keys()
    for name, trait in expected.items():
        assert trait in ids[name], (name, ids[name])
    assert expected['argv.py'] not in ids['negative.py']
    assert not any(i.startswith('micro-behaviors/process/deploy/interpreter-command::') and
                   i.rsplit('::', 1)[-1] in {x.rsplit('::', 1)[-1] for x in expected.values()}
                   for file_ids in ids.values() for i in file_ids)
    print('Command construction and unbound inputs retain their evidence traits.')
