#!/usr/bin/env python3
"""Check retained theft coverage and neutral near misses without execution."""
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
cases = json.loads(Path(__file__).with_name('cases.json').read_text())['fixtures']
engine = os.environ.get('CLEAVE', 'cleave')
result = subprocess.run([engine, '--traits-dir', '.', '--json', *[c['path'] for c in cases]],
                        cwd=ROOT, text=True, capture_output=True)
if result.returncode:
    raise SystemExit(result.stderr)
files = {str(Path(f['path']).resolve()): f for line in result.stdout.splitlines()
         for f in json.loads(line)['files']}
for case in cases:
    file = files[str((ROOT / case['path']).resolve())]
    actual = {t['id']: t['crit'] for t in file.get('traits', [])}
    for trait in case['matched']:
        assert trait in actual, (case['path'], 'missing', trait)
    for trait in case['not_matched']:
        assert trait not in actual, (case['path'], 'unexpected', trait)
    if 'max_criticality' in case:
        assert max(actual.values(), default=0) <= case['max_criticality'], (case['path'], actual)
    print('PASS', case['path'])
