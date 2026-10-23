#!/usr/bin/env python3
"""Run positive and near-miss source relationship controls without execution."""
import json
import os
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[3]
cases = json.loads(Path(__file__).with_name('cases.json').read_text())['fixtures']
run = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(root),
                      '--format', 'jsonl', *[str(root / c['path']) for c in cases]],
                     text=True, capture_output=True, check=True)
reports = {}
for line in run.stdout.splitlines():
    for file in json.loads(line).get('files', []):
        reports[Path(file['path']).name] = {t['id'] for t in file.get('traits', [])}
failed = []
for case in cases:
    traits = reports.get(Path(case['path']).name, set())
    missing = sorted(set(case['matched']) - traits)
    unexpected = sorted(set(case['not_matched']) & traits)
    if missing or unexpected:
        failed.append({'case': case['case_id'], 'missing': missing, 'unexpected': unexpected})
if failed:
    print(json.dumps(failed, indent=2))
    sys.exit(1)
print(f'{len(cases)} source relationship controls passed')
