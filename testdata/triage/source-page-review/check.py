#!/usr/bin/env python3
"""Check focused source-page positive and near-miss fixtures."""
import json
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[3]
cases = json.loads((Path(__file__).parent / 'cases.json').read_text())['fixtures']
result = subprocess.run(
    [sys.argv[1] if len(sys.argv) > 1 else 'cleave', '--traits-dir', '.',
     '--format', 'json', *(case['path'] for case in cases)],
    cwd=root, capture_output=True, text=True, check=True,
)
# Multi-target output may contain adjacent JSON documents rather than JSONL.
decoder = json.JSONDecoder()
remaining = result.stdout.lstrip()
files = {}
while remaining:
    document, end = decoder.raw_decode(remaining)
    for file in document.get('files', []):
        files[Path(file['path']).name] = file.get('traits', [])
    remaining = remaining[end:].lstrip()
failures = []
for case in cases:
    traits = files.get(Path(case['path']).name)
    if traits is None:
        failures.append(f"{case['path']}: absent report")
        continue
    actual = {trait['id'] for trait in traits}
    missing = set(case['matched']) - actual
    unexpected = set(case['not_matched']) & actual
    if missing or unexpected:
        failures.append(f"{case['path']}: missing={sorted(missing)}, unexpected={sorted(unexpected)}")
    if case.get('max_crit') is not None:
        excessive = [trait['id'] for trait in traits if trait['crit'] > case['max_crit']]
        if excessive:
            failures.append(f"{case['path']}: excessive criticality={excessive}")
for failure in failures:
    print(failure)
print(f'{len(cases)} fixtures; {len(failures)} failures')
if result.stderr:
    print(result.stderr, file=sys.stderr)
raise SystemExit(bool(failures))
