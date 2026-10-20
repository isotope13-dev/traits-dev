#!/usr/bin/env python3
"""Check neutral source/build coverage and nearby false positives."""
import json
import pathlib
import subprocess
import sys

root = pathlib.Path(__file__).resolve().parents[3]
cases = json.loads(pathlib.Path(__file__).with_name('cases.json').read_text())
result = subprocess.run(
    [sys.argv[1] if len(sys.argv) > 1 else 'cleave', '--traits-dir', str(root),
     '--format', 'json', str(pathlib.Path(__file__).parent)],
    cwd=root, text=True, capture_output=True, check=True)
if result.stderr.strip():
    raise SystemExit(result.stderr)
remaining = result.stdout
reports = {}
decoder = json.JSONDecoder()
while remaining.strip():
    report, end = decoder.raw_decode(remaining.lstrip())
    remaining = remaining.lstrip()[end:]
    for file in report['files']:
        reports[pathlib.Path(file['path']).name] = {
            trait['id'] for trait in file.get('traits', [])}
failures = []
for case in cases['fixtures']:
    actual = reports.get(pathlib.Path(case['path']).name, set())
    missing = set(case['required_emitted']) - actual
    unexpected = set(case['forbidden_emitted']) & actual
    if missing or unexpected:
        failures.append((case['case_id'], sorted(missing), sorted(unexpected)))
if failures:
    raise SystemExit(json.dumps(failures, indent=2))
print(f"PASS: {len(cases['fixtures'])} runtime, compiler, and libc controls")
