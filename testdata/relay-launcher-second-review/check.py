#!/usr/bin/env python3
"""Check inert source fixtures without test-directory context exclusions."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--scratch', type=Path, required=True)
args = parser.parse_args()
fixtures = Path(__file__).resolve().parent
root = fixtures.parents[1]
cases = json.loads((fixtures / 'cases.json').read_text())
args.scratch.mkdir(parents=True, exist_ok=True)
for case in cases:
    shutil.copyfile(fixtures / case['name'], args.scratch / case['name'])
result = subprocess.run(
    ['cleave', '--traits-dir', str(root), '--json', str(args.scratch)],
    capture_output=True, text=True, check=True)
reports = {}
for line in result.stdout.splitlines():
    for entry in json.loads(line)['files']:
        reports[Path(entry['path']).name] = entry
for case in cases:
    entry = reports[case['name']]
    actual = {trait['id'] for trait in entry.get('traits', [])}
    missing = set(case['matched']) - actual
    unexpected = set(case['not_matched']) & actual
    assert not missing and not unexpected, (case['name'], missing, unexpected)
    if case['name'] != 'relay-stage.ps1':
        assert not any(t['crit'] >= 4 for t in entry.get('traits', [])), case['name']
    print('PASS', case['name'])
