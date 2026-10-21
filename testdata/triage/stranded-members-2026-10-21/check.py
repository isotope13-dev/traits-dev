#!/usr/bin/env python3
"""Check storage-reference placement without executing fixture code."""
import argparse
import json
from pathlib import Path
import subprocess

here = Path(__file__).resolve().parent
root = here.parents[2]
parser = argparse.ArgumentParser()
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
cases = json.loads((here / 'cases.json').read_text())
paths = [str((here / case['file']).resolve()) for case in cases]
run = subprocess.run([args.cleave, '--traits-dir', str(root), '--json', *paths],
                     check=True, capture_output=True, text=True)
reports = {str(Path(f['path']).resolve()): f
           for line in run.stdout.splitlines()
           for f in json.loads(line)['files']}
for case, path in zip(cases, paths):
    traits = {t['id']: t['crit'] for t in reports[path].get('traits', [])}
    missing = set(case['present']) - traits.keys()
    unwanted = set(case['absent']) & traits.keys()
    assert not missing and not unwanted, (case['file'], missing, unwanted)
    assert not any(c >= 4 for c in traits.values()), (case['file'], traits)
    # OR selector groups can be filtered from scan presentation; test their
    # matcher directly so the referenced capability is verified as retained.
    for trait in case.get('matches', []):
        debug = subprocess.run([args.cleave, '--traits-dir', str(root),
                                'test-rules', path, '--rules', trait],
                               check=True, capture_output=True, text=True)
        assert f'MATCHED {trait} ' in debug.stdout, debug.stdout
    print('PASS', case['file'])
