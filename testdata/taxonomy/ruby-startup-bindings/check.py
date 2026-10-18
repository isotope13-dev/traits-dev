#!/usr/bin/env python3
"""Scan static fixtures; check installation bindings without executing Ruby."""
import json
import os
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[3]
cases = json.loads(Path(__file__).with_name('cases.json').read_text())['fixtures']
result = subprocess.run(
    [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(root),
     '--format', 'json', *[case['path'] for case in cases]],
    cwd=root, text=True, capture_output=True, check=True,
)
decoder = json.JSONDecoder()
remaining = result.stdout
files = {}
while remaining.strip():
    report, end = decoder.raw_decode(remaining.lstrip())
    remaining = remaining.lstrip()[end:]
    files.update({entry['path']: entry for entry in report['files']})
for case in cases:
    actual = {trait['id'] for trait in files[case['path']].get('traits', [])}
    missing = set(case['required_emitted']) - actual
    forbidden = set(case['forbidden_emitted']) & actual
    assert not missing and not forbidden, (case['case_id'], missing, forbidden)
print(f"All {len(cases)} Ruby startup binding controls passed")
