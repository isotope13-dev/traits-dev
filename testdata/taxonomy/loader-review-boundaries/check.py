#!/usr/bin/env python3
"""Check required capabilities and UAC-bypass admission without executing fixtures."""
import argparse
import json
import os
from pathlib import Path
import subprocess

here = Path(__file__).resolve().parent
root = here.parents[2]
parser = argparse.ArgumentParser()
parser.add_argument('--report', type=Path, help='Check an existing cleave JSON report')
args = parser.parse_args()
cases = json.loads((here / 'cases.json').read_text())['fixtures']
if args.report:
    output = args.report.read_text()
else:
    output = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(root),
         '--format', 'json', 'analyze'] + [str(root / x['path']) for x in cases],
        check=True, capture_output=True, text=True,
    ).stdout
findings = {}
decoder = json.JSONDecoder()
while output.strip():
    report, end = decoder.raw_decode(output.lstrip())
    output = output.lstrip()[end:]
    for file in report['files']:
        findings[Path(file['path']).name] = {x['id'] for x in file.get('traits', [])}
checks = 0
for case in cases:
    actual = findings[Path(case['path']).name]
    for trait in case.get('matched', []):
        assert trait in actual, (case['case_id'], 'missing', trait)
        checks += 1
    for trait in case.get('not_matched', []):
        assert trait not in actual, (case['case_id'], 'unexpected', trait)
        checks += 1
print(f'Passed {len(cases)} controls, {checks} assertions')
