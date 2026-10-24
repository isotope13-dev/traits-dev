#!/usr/bin/env python3
"""Check bound static observations without running any specimen code."""
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
result = subprocess.run(
    [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
     '--format', 'json', str(HERE)], capture_output=True, text=True)
assert result.returncode in (0, 1, 2), result.stderr
assert 'validation failed' not in result.stdout, result.stdout
assert 'Warning:' not in result.stderr, result.stderr
files = {}
remaining = result.stdout
while remaining.strip():
    report, end = json.JSONDecoder().raw_decode(remaining.lstrip())
    remaining = remaining.lstrip()[end:]
    for f in report['files']:
        files[Path(f['path']).name] = {t['id']: t for t in f.get('traits', [])}
checks = 0
for case in json.loads((HERE / 'cases.json').read_text()):
    found = files[case['file']]
    for trait in case['present']:
        assert trait in found, (case['file'], 'missing', trait)
        checks += 1
    for trait in case['absent']:
        assert trait not in found, (case['file'], 'unexpected', trait)
        checks += 1
print(f'{checks} assertions passed across {len(json.loads((HERE / "cases.json").read_text()))} cases')
