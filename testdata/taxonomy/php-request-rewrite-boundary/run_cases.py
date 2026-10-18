#!/usr/bin/env python3
"""Check PHP injection bindings and metadata-preserving near misses."""
import json
import subprocess
import sys
from pathlib import Path

cases = json.loads(Path(__file__).with_name('cases.json').read_text())['fixtures']
result = subprocess.run(
    [sys.argv[1] if len(sys.argv) > 1 else 'cleave', '--traits-dir', '.',
     '--format', 'json', *[case['path'] for case in cases]],
    capture_output=True, text=True, check=True,
)
reports = {}
remaining = result.stdout
while remaining.strip():
    report, end = json.JSONDecoder().raw_decode(remaining.lstrip())
    remaining = remaining.lstrip()[end:]
    for item in report['files']:
        reports[item['path']] = {trait['id']: trait for trait in item['traits']}
errors = []
for case in cases:
    traits = reports[case['path']]
    errors += [f"{case['path']}: missing {trait}" for trait in case['matched'] if trait not in traits]
    errors += [f"{case['path']}: unexpected {trait}" for trait in case['not_matched'] if trait in traits]
    if case['path'].startswith('testdata/benign/'):
        errors += [f"{case['path']}: hostile {trait}" for trait, finding in traits.items() if finding['crit'] >= 5]
if errors:
    raise SystemExit('\n'.join(errors))
print(f"PASS: {len(cases)} PHP injection and near-miss cases")
