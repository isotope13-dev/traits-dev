#!/usr/bin/env python3
"""Static controls for corrected claims and retained charcode attack coverage."""
import argparse
import shutil
import json
import os
from pathlib import Path
import shlex
import subprocess

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
cases = json.loads((HERE / 'cases.json').read_text())['fixtures']
parser = argparse.ArgumentParser()
parser.add_argument('--scratch', type=Path, required=True)
args = parser.parse_args()
args.scratch.mkdir(parents=True, exist_ok=True)
paths = []
for i, case in enumerate(cases):
    target = args.scratch / f'{i:02d}-{Path(case["path"]).name}'
    shutil.copyfile(ROOT / case['path'], target)
    paths.append(target)
# The helper intentionally excludes test directories. Copy controls to the
# supplied scratch path to exercise production matching, retaining suffixes.
command = shlex.split(os.environ.get('CLEAVE', 'cleave'))
result = subprocess.run(command + ['--traits-dir', str(ROOT), '--json'] +
                        list(map(str, paths)),
                        check=True, capture_output=True, text=True)
files = [file for line in result.stdout.splitlines() if line.strip()
         for file in json.loads(line)['files']]
by_path = {file['path']: file for file in files}
for case, path in zip(cases, paths):
    file = by_path[str(path)]
    traits = {trait['id']: trait for trait in file.get('traits', [])}
    assert set(case.get('matched', [])) <= traits.keys(), (case['path'], traits.keys())
    assert not set(case.get('not_matched', [])) & traits.keys(), (case['path'], traits.keys())
    for name, crit in case.get('levels', {}).items():
        assert traits[name]['crit'] == crit, (case['path'], name, traits[name]['crit'])
    print(Path(case['path']).name + ': passed')
print(f'{len(cases)} static controls passed')
