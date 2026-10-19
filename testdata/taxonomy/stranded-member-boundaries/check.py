#!/usr/bin/env python3
"""Check neutral capability and request-to-command boundaries without execution."""
import json
import os
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[3]
cases = json.loads(Path(__file__).with_name('cases.json').read_text())['fixtures']
engine = os.environ.get('CLEAVE', 'cleave')
result = subprocess.run(
    [engine, '--traits-dir', str(root), '--format', 'json',
     *[case['path'] for case in cases]],
    cwd=root, text=True, capture_output=True, check=True,
)
if result.stderr.strip():
    print(result.stderr, file=sys.stderr)
reports = []
decoder = json.JSONDecoder()
pending = result.stdout.lstrip()
while pending:
    report, end = decoder.raw_decode(pending)
    reports.append(report)
    pending = pending[end:].lstrip()
files = {entry['path']: entry for report in reports for entry in report['files']}
for case in cases:
    findings = {item['id']: item for item in files[case['path']]['traits']}
    assert set(case['matched']) <= findings.keys(), case['path']
    assert not set(case['not_matched']) & findings.keys(), case['path']
    assert all(item['crit'] <= case['max_criticality'] for item in findings.values()), case['path']
print(f'{len(cases)} boundary controls passed')
