#!/usr/bin/env python3
"""Check static findings against behavior controls; never run the fixtures."""
import argparse
import json
import subprocess
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
directory = Path(__file__).resolve().parent
root = directory.parents[2]
cases = json.loads((directory / 'cases.json').read_text())['fixtures']
scan = subprocess.run(
    [args.cleave, '--traits-dir', str(root), '--format', 'json',
     *[case['path'] for case in cases]],
    cwd=root, capture_output=True, text=True,
)
if scan.returncode:
    raise SystemExit(scan.stderr or scan.stdout)
remaining = scan.stdout.strip()
files = {}
while remaining:
    report, end = json.JSONDecoder().raw_decode(remaining)
    for file in report['files']:
        files[file['path']] = {trait['id'] for trait in file.get('traits', [])}
    remaining = remaining[end:].lstrip()
for case in cases:
    actual = files[case['path']]
    for trait in case['matched']:
        assert trait in actual, (case['case_id'], 'missing', trait)
    for trait in case['not_matched']:
        assert trait not in actual, (case['case_id'], 'unexpected', trait)
print(f"Passed {len(cases)} positive and near-miss controls")
