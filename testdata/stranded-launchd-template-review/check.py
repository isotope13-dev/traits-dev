#!/usr/bin/env python3
"""Check static template observations; never execute the fixture programs."""
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
cases = json.loads((HERE / 'cases.json').read_text())
result = subprocess.run(
    [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
     '--format', 'json'] + [str(HERE / c['file']) for c in cases],
    capture_output=True, text=True, check=True,
)
assert not result.stderr.strip(), result.stderr
reports = {}
remaining = result.stdout
while remaining.strip():
    report, end = json.JSONDecoder().raw_decode(remaining.lstrip())
    remaining = remaining.lstrip()[end:]
    for file in report['files']:
        reports[Path(file['path']).name] = file
checks = 0
for case in cases:
    traits = {t['id']: t for t in reports[case['file']].get('traits', [])}
    for trait, expected in case['expected'].items():
        assert (trait in traits) == expected, (case['file'], trait, expected)
        checks += 1
    if case['forbidden_hostile']:
        assert not [t for t in traits.values() if t['crit'] == 5], case['file']
        checks += 1
print(f'{checks} assertions passed across {len(cases)} static templates')
