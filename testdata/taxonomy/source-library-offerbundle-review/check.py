#!/usr/bin/env python3
"""Check real launch operations against UI/library near misses."""
import json
import os
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[3]
cases = json.loads(Path(__file__).with_name('cases.json').read_text())['fixtures']
command = [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(root), '--format', 'jsonl']
command.extend(case['path'] for case in cases)
result = subprocess.run(command, cwd=root, text=True, capture_output=True, check=True)
decoder = json.JSONDecoder()
remaining = result.stdout.strip()
files = {}
while remaining:
    report, offset = decoder.raw_decode(remaining)
    for item in report['files']:
        files[item['path']] = {trait['id'] for trait in item.get('traits', [])}
    remaining = remaining[offset:].lstrip()
failures = []
for case in cases:
    ids = files.get(case['path'], set())
    missing = set(case['required_emitted']) - ids
    extra = set(case['forbidden_emitted']) & ids
    if case['path'] not in files or missing or extra:
        failures.append((case['case_id'], sorted(missing), sorted(extra)))
if failures:
    raise SystemExit(str(failures))
print(f"Passed {len(cases)} source and library boundary controls")
