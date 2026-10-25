"""Check static rule controls; never execute any fixture or recovered code.

Run from the repository root: python3 testdata/triage/http-miasma-second-review/verify.py
Optional first argument: extracted recovered/ directory for real-source checks.
"""
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
cases = json.loads((HERE / 'cases.json').read_text())
inputs = [HERE / row['path'] for row in cases]
legacy = ROOT / 'testdata/testmetest-miasma/controls'
inputs.extend(p for p in legacy.rglob('*') if p.is_file())
if len(sys.argv) > 1:
    recovered = Path(sys.argv[1]).resolve()
    for filename, required in [
        ('functions/18-dollarr.js', 'micro-behaviors/os/package-manager/archive::javascript-wheel-pth-member-assignment'),
        ('functions/25-Zn.js', 'micro-behaviors/data/format/credentials::javascript-padded-github-pat-construction'),
        ('payload.js', 'objectives/supply-chain/trojanized/build-pipeline::pypi-pth-member-republisher'),
    ]:
        inputs.append(recovered / filename)
        cases.append({'path': str(recovered / filename), 'required': [required], 'forbidden': []})
result = subprocess.run(
    [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT), '--format', 'json', *map(str, inputs)],
    text=True, capture_output=True, check=True)
decoder, remaining, files = json.JSONDecoder(), result.stdout, []
while remaining.strip():
    report, end = decoder.raw_decode(remaining.lstrip())
    remaining = remaining.lstrip()[end:]
    files.extend(report.get('files', []))
failures = []
for row in cases:
    expected_path = str((HERE / row['path']).resolve())
    selected = [f for f in files if str(Path(f['path']).resolve()) == expected_path]
    ids = {t['id'] for f in selected for t in f.get('traits', [])}
    missing = set(row['required']) - ids
    unexpected = set(row['forbidden']) & ids
    if not selected or missing or unexpected:
        failures.append({'path': row['path'], 'missing': sorted(missing), 'unexpected': sorted(unexpected)})
for file in files:
    if str(legacy) in file['path']:
        failures.extend({'path': file['path'], 'unexpected': t['id']}
                        for t in file.get('traits', []) if t['crit'] >= 4)
if failures:
    raise SystemExit(json.dumps(failures, indent=2))
print(f'PASS: {len(cases)} focused assertions; existing controls have no high findings')
