#!/usr/bin/env python3
"""Check static sector-write operands; never execute the JavaScript fixtures."""
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
cases = json.loads((HERE / 'cases.json').read_text())
targets = sorted({str((HERE / case['file']).resolve()) for case in cases})
result = subprocess.run([
    os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
    '--format', 'json', *targets,
], capture_output=True, text=True)
assert result.returncode in (0, 1, 2), result.stderr
assert not result.stderr.strip(), result.stderr
files = {}
remaining = result.stdout
while remaining.strip():
    report, end = json.JSONDecoder().raw_decode(remaining.lstrip())
    remaining = remaining.lstrip()[end:]
    for unit in report['files']:
        files[str(Path(unit['path']).resolve())] = {
            trait['id'] for trait in unit.get('traits', [])
        }
checks = 0
for case in cases:
    actual = files[str((HERE / case['file']).resolve())]
    for trait in case['present']:
        assert trait in actual, (case['file'], 'missing', trait)
        checks += 1
    for trait in case['absent']:
        assert trait not in actual, (case['file'], 'unexpected', trait)
        checks += 1
print(f'{checks} assertions passed across {len(cases)} cases')
