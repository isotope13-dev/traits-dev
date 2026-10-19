#!/usr/bin/env python3
"""Check reference boundaries and retain POST evidence without inferring upload."""
import json
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
manifest = json.loads((HERE / 'cases.json').read_text())
result = subprocess.run(
    [sys.argv[1] if len(sys.argv) > 1 else 'cleave', '--traits-dir', str(ROOT),
     '--disable', 'third-party', '--format', 'json', str(HERE)],
    capture_output=True, text=True, check=True,
)
decoder = json.JSONDecoder()
remaining = result.stdout.strip()
reports = {}
while remaining:
    report, end = decoder.raw_decode(remaining)
    for file in report['files']:
        reports[pathlib.Path(file['path']).name] = file
    remaining = remaining[end:].lstrip()

for case in manifest['fixtures']:
    file = reports[pathlib.Path(case['path']).name]
    ids = {trait['id'] for trait in file['traits']}
    missing = set(case['required_emitted']) - ids
    forbidden = (set(case['forbidden_emitted']) | set(manifest['retired_ids'])) & ids
    assert not missing, (case['case_id'], 'missing', sorted(missing))
    assert not forbidden, (case['case_id'], 'forbidden', sorted(forbidden))
    assert not [trait for trait in file['traits'] if trait['crit'] >= 4], case['case_id']
    print('PASS', case['case_id'])
