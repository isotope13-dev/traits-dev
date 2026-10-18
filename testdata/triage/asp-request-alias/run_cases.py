#!/usr/bin/env python3
"""Check request-to-Eval alias bindings in Classic ASP."""
import argparse
import json
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
root = Path(__file__).resolve().parents[3]
cases = json.loads(Path(__file__).with_name('cases.json').read_text())['cases']
result = subprocess.run(
    [args.cleave, '--traits-dir', str(root), '--format', 'json']
    + [str(root / case['path']) for case in cases],
    check=True, capture_output=True, text=True, cwd=root,
)
reports = {}
decoder = json.JSONDecoder()
pending = result.stdout.strip()
while pending:
    report, end = decoder.raw_decode(pending)
    for file in report['files']:
        reports[str(Path(file['path']).resolve())] = file
    pending = pending[end:].lstrip()
failures = []
for case in cases:
    file = reports[str((root / case['path']).resolve())]
    traits = {trait['id'] for trait in file.get('traits', [])}
    for trait in case['required']:
        if trait not in traits:
            failures.append(f"{case['path']}: missing {trait}")
    for trait in case['forbidden']:
        if trait in traits:
            failures.append(f"{case['path']}: unexpected {trait}")
if failures:
    raise SystemExit('\n'.join(failures))
print(f"Passed {len(cases)} Classic ASP alias controls")
