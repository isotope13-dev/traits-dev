#!/usr/bin/env python3
"""Exercise real/imitated Google assets, AJAX methods, and language placement."""
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
cases = json.loads((HERE / 'cases.json').read_text())['fixtures']
result = subprocess.run(
    [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
     '--format', 'json', *[str(ROOT / c['path']) for c in cases]],
    cwd=ROOT, check=True, capture_output=True, text=True,
)
# The CLI emits concatenated report objects for multiple input files.
decoder = json.JSONDecoder()
remaining = result.stdout
reports = {}
while remaining.strip():
    remaining = remaining.lstrip()
    report, end = decoder.raw_decode(remaining)
    remaining = remaining[end:]
    for item in report['files']:
        reports[Path(item['path']).name] = {t['id'] for t in item.get('traits', [])}
for case in cases:
    observed = reports[Path(case['path']).name]
    missing = set(case['matched']) - observed
    unexpected = set(case['not_matched']) & observed
    assert not missing and not unexpected, (case['path'], missing, unexpected)
print(f'{len(cases)} positive and near-miss controls passed')
