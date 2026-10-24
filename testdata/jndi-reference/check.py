#!/usr/bin/env python3
"""Check JNDI source variants and nearby safe configurations against local rules."""
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CASES = json.loads((HERE / 'cases.json').read_text())
if len(sys.argv) > 1:
    report = Path(sys.argv[1]).read_text()
else:
    result = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT), '--json', str(HERE)],
        check=True, capture_output=True, text=True,
    )
    report = result.stdout
observed = {}
for line in report.splitlines():
    for entry in json.loads(line).get('files', []):
        observed[Path(entry['path']).name] = {trait['id'] for trait in entry.get('traits', [])}
errors = []
for case in CASES:
    found = observed.get(case['file'])
    if found is None:
        errors.append(f"Missing scan: {case['file']}")
        continue
    for trait in case.get('matched', []):
        if trait not in found:
            errors.append(f"{case['file']}: missed {trait}")
    for trait in case.get('not_matched', []):
        if trait in found:
            errors.append(f"{case['file']}: unexpected {trait}")
if errors:
    print('\n'.join(errors), file=sys.stderr)
    raise SystemExit(1)
print(f'{len(CASES)} JNDI variant and precision cases passed')
