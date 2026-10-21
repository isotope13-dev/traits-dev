#!/usr/bin/env python3
"""Run the source-listing positive and near-miss controls."""
import json
import os
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[3]
cases = json.loads(Path(__file__).with_name('cases.json').read_text())['fixtures']
result = subprocess.run(
    [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(root),
     '--format', 'json', *[str(root / case['path']) for case in cases]],
    check=True, text=True, capture_output=True)
# Multi-input JSON reports can be concatenated without separating newlines.
remaining = result.stdout.strip()
reports = {}
decoder = json.JSONDecoder()
while remaining:
    report, end = decoder.raw_decode(remaining)
    for file in report['files']:
        reports[Path(file['path']).name] = {t['id'] for t in file.get('traits', [])}
    remaining = remaining[end:].lstrip()
for case in cases:
    name = Path(case['path']).name
    ids = reports[name]
    missing = set(case['matched']) - ids
    unexpected = set(case['not_matched']) & ids
    if missing or unexpected:
        raise AssertionError((name, sorted(missing), sorted(unexpected)))
    print(f'PASS {name}')
