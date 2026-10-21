#!/usr/bin/env python3
"""Static controls for the stranded-member trait corrections; executes no fixture."""
import json
import os
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[3]
cases = json.loads(Path(__file__).with_name('cases.json').read_text())
env = os.environ.copy()
env.pop('CLEAVE_VALIDATE', None)
engine = sys.argv[1] if len(sys.argv) > 1 else 'cleave'
paths = [str(root / case['path']) for case in cases['fixtures']]
result = subprocess.run([engine, '--traits-dir', str(root), '--format', 'json', *paths],
                        env=env, capture_output=True, text=True, check=True)
reports = []
remaining = result.stdout.lstrip()
decoder = json.JSONDecoder()
while remaining:
    report, end = decoder.raw_decode(remaining)
    reports.append(report)
    remaining = remaining[end:].lstrip()
files = {Path(f['path']).resolve(): f for report in reports for f in report['files']}
for case, path in zip(cases['fixtures'], paths):
    traits = files[Path(path).resolve()]['traits']
    ids = {t['id'] for t in traits}
    missing = set(case['matched']) - ids
    unexpected = set(case['not_matched']) & ids
    hostile = [t['id'] for t in traits if t['crit'] == 5]
    assert not (missing or unexpected or hostile), (case['case_id'], missing, unexpected, hostile)
    print('PASS', case['case_id'])
