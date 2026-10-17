#!/usr/bin/env python3
"""Check declared requests vs definitions and ordinary analyzer fixture APIs."""
import json, os, pathlib, subprocess
cases = json.loads(pathlib.Path(__file__).with_name('cases.json').read_text())
for case in cases['fixtures']:
    result = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', '.', '--format', 'json', case['path']], capture_output=True, text=True, check=True)
    report = json.loads(result.stdout)
    ids = {t['id'] for f in report['files'] for t in f.get('traits', [])}
    missing = set(case['matched']) - ids
    extra = set(case['not_matched']) & ids
    high = [(t['crit'], t['id']) for f in report['files'] for t in f.get('traits', []) if t['crit'] >= 4]
    assert not missing and not extra and not high, (case['path'], missing, extra, high)
    print('PASS', case['path'])
