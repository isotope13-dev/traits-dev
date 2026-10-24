#!/usr/bin/env python3
"""Check reviewed matcher boundaries, using fresh or recorded Cleave reports."""
import argparse
import json
import os
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--report', action='append', type=Path, default=[])
args = parser.parse_args()
here = Path(__file__).resolve().parent
repo = here.parents[2]
cases = json.loads((here / 'cases.json').read_text())
reports = []
if args.report:
    reports = [p.read_text() for p in args.report]
else:
    run = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(repo),
         'analyze', '--format', 'jsonl',
         *[str(here / c['file']) for c in cases]],
        check=True, text=True, capture_output=True)
    reports = [run.stdout]
by_path = {}
for report in reports:
    for line in report.splitlines():
        if not line.strip():
            continue
        data = json.loads(line)
        for f in data.get('raw', data).get('files', []):
            by_path[Path(f['path']).resolve()] = f
for case in cases:
    f = by_path[(here / case['file']).resolve()]
    traits = f.get('traits', [])
    ids = {t['id'] for t in traits}
    for trait in case.get('present', []):
        assert trait in ids, (case['file'], 'missing', trait)
    for trait in case.get('absent', []):
        assert trait not in ids, (case['file'], 'unexpected', trait)
    if case.get('no_hostile'):
        assert not any(t['crit'] == 5 for t in traits), case['file']
    print('PASS', case['file'])
