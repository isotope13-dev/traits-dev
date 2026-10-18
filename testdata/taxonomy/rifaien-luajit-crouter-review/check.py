#!/usr/bin/env python3
"""Focused controls: inspect files statically; never execute fixture code."""
import json
import pathlib
import subprocess
import sys

root = pathlib.Path(__file__).resolve().parents[3]
base = pathlib.Path(__file__).resolve().parent
cleave = sys.argv[1] if len(sys.argv) > 1 else 'cleave'
for case in json.loads((base / 'cases.json').read_text())['fixtures']:
    result = subprocess.run(
        [cleave, '--traits-dir', str(root), '--format', 'json', str(base / case['path'])],
        capture_output=True, text=True, check=True,
    )
    report = json.loads(result.stdout)
    traits = report['files'][0].get('traits', [])
    ids = {t['id'] for t in traits}
    missing = set(case.get('matched', [])) - ids
    unexpected = set(case.get('not_matched', [])) & ids
    assert not missing and not unexpected, (case['path'], missing, unexpected)
    assert not any(t['crit'] >= 5 for f in report['files'] for t in f.get('traits', [])), case['path']
    suspicious = {t['id'] for f in report['files'] for t in f.get('traits', []) if t['crit'] == 4}
    assert len(suspicious) <= case.get('max_suspicious', 0), (case['path'], suspicious)
    print('PASS', case['path'])
