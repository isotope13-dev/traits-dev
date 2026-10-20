"""Scan inert source fixtures and verify admission and near-miss boundaries."""
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
cases = json.loads((HERE / 'cases.json').read_text())['fixtures']
# These fixtures are scanned as data; no sample or fixture is executed.
command = [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
           '--format', 'json', *[str(ROOT / c['path']) for c in cases]]
run = subprocess.run(command, text=True, capture_output=True, cwd=ROOT)
if run.returncode:
    raise SystemExit(run.stderr or run.stdout)
reports = []
remaining = run.stdout.lstrip()
decoder = json.JSONDecoder()
while remaining:
    report, end = decoder.raw_decode(remaining)
    reports.append(report)
    remaining = remaining[end:].lstrip()
files = {str(Path(f['path']).resolve()): f
         for report in reports for f in report['files']}
errors = []
for case in cases:
    file = files.get(str((ROOT / case['path']).resolve()))
    if file is None:
        errors.append(f"{case['case_id']}: no file report")
        continue
    traits = {t['id']: t for t in file.get('traits', [])}
    for trait in case.get('matched', []):
        if trait not in traits:
            errors.append(f"{case['case_id']}: missing {trait}")
    for trait in case.get('not_matched', []):
        if trait in traits:
            errors.append(f"{case['case_id']}: unexpected {trait}")
    ceiling = case.get('max_crit')
    if ceiling is not None:
        for trait in traits.values():
            if trait['crit'] > ceiling:
                errors.append(f"{case['case_id']}: excessive severity {trait['id']}")
if errors:
    raise SystemExit('\n'.join(errors))
print(f"PASS: {len(cases)} source and command admission controls")
