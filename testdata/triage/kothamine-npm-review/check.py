#!/usr/bin/env python3
"""Focused rule coverage and nearby benign controls; run from any directory."""
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
cases = json.loads((HERE / 'cases.json').read_text())
result = subprocess.run(
    [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT), '--json',
     *[case['path'] for case in cases]],
    cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
)
if result.returncode:
    raise SystemExit(result.stderr)
files = [file for line in result.stdout.splitlines()
         for file in json.loads(line)['files']]
failures = []
for case in cases:
    prefix = case['path']
    matched_files = [file for file in files
                     if file['path'] == prefix
                     or file['path'].startswith(prefix + '!!')]
    if not matched_files:
        failures.append({'path': prefix, 'error': 'missing report'})
        continue
    found = {trait['id'] for file in matched_files
             for trait in file.get('traits', [])}
    for trait in case['matched']:
        if trait not in found:
            failures.append({'path': prefix, 'missing': trait})
    for trait in case['not_matched']:
        if trait in found:
            failures.append({'path': prefix, 'unexpected': trait})
print(json.dumps({'cases': len(cases), 'failures': failures}, indent=2))
raise SystemExit(bool(failures))
