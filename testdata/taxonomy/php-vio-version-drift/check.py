#!/usr/bin/env python3
"""Scan source fixtures without executing their contents."""
import json
import os
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[3]
cases = json.loads(Path(__file__).with_name('cases.json').read_text())
result = subprocess.run(
    [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(root), '--format', 'json',
     *[str(root / case['path']) for case in cases]],
    check=True, capture_output=True, text=True,
)
reports = []
remaining = result.stdout.lstrip()
decoder = json.JSONDecoder()
while remaining:
    document, end = decoder.raw_decode(remaining)
    reports.extend(document['files'])
    remaining = remaining[end:].lstrip()
if os.environ.get('VIO_CASE_REPORT'):
    Path(os.environ['VIO_CASE_REPORT']).write_text(json.dumps(reports))
errors = []
for case in cases:
    path = str(root / case['path'])
    matching = [report for report in reports if report['path'] == path]
    assert matching, f"missing report: {path}"
    traits = {trait['id'] for report in matching for trait in report.get('traits', [])}
    for trait in case['required']:
        if trait not in traits:
            errors.append(f"{path}: missing {trait}")
    for prefix in case['forbidden']:
        unexpected = sorted(trait for trait in traits if trait.startswith(prefix))
        if unexpected:
            errors.append(f"{path}: unexpected {unexpected}")
assert not errors, '\n'.join(errors)
print(f'{len(cases)} focused cases passed')
