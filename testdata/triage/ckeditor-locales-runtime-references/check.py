#!/usr/bin/env python3
"""Check identity versus behavior boundaries and preserved metadata observations."""
import json
import pathlib
import subprocess

root = pathlib.Path(__file__).resolve().parents[3]
cases = json.loads(pathlib.Path(__file__).with_name('cases.json').read_text())['fixtures']
result = subprocess.run(
    ['cleave', '--traits-dir', str(root), '--format', 'json'] +
    [str(root / case['path']) for case in cases],
    check=True, text=True, capture_output=True,
)
remaining = result.stdout
reports = {}
decoder = json.JSONDecoder()
while remaining.strip():
    report, end = decoder.raw_decode(remaining.lstrip())
    remaining = remaining.lstrip()[end:]
    for file in report['files']:
        reports[pathlib.Path(file['path']).name] = {t['id'] for t in file.get('traits', [])}
for case in cases:
    actual = reports[pathlib.Path(case['path']).name]
    missing = set(case['required_emitted']) - actual
    unexpected = set(case['forbidden_emitted']) & actual
    assert not missing and not unexpected, (case['path'], missing, unexpected)
    print('PASS', pathlib.Path(case['path']).name)
