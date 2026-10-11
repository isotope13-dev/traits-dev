#!/usr/bin/env python3
"""Verify positive and near-miss traits without executing fixture content."""
import json
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parent.parent
cases = json.loads((root / 'testdata/pypykatz-fortnight/cases.json').read_text())['fixtures']
result = subprocess.run(
    ['cleave', '--traits-dir', str(root), '--all-files', '--json', *[str(root / c['path']) for c in cases]],
    capture_output=True, text=True, check=True,
)
files = {}
for line in result.stdout.splitlines():
    for item in json.loads(line)['files']:
        files[Path(item['path']).name] = {t['id'] for t in item.get('traits', [])}
errors = []
for case in cases:
    name = Path(case['path']).name
    actual = files.get(name, set())
    missing = set(case['matched']) - actual
    unexpected = set(case['not_matched']) & actual
    if missing or unexpected or name not in files:
        errors.append(f'{name}: missing={sorted(missing)}, unexpected={sorted(unexpected)}')
if errors:
    raise SystemExit('\n'.join(errors))
print(f'Passed {len(cases)} positive and near-miss cases')
