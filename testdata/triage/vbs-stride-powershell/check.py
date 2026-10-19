#!/usr/bin/env python3
"""Check placement, near misses, and severity without running VBScript."""
import argparse
import json
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
root = Path(__file__).resolve().parents[3]
fixtures = Path(__file__).resolve().parent
cases = json.loads((fixtures / 'cases.json').read_text())
result = subprocess.run(
    [args.cleave, '--traits-dir', str(root), '--format', 'json',
     *[str(fixtures / case['path']) for case in cases]],
    text=True, capture_output=True, check=True,
)
# Multi-file CLI output consists of adjacent JSON report objects.
decoder = json.JSONDecoder()
remaining = result.stdout.strip()
files = {}
while remaining:
    report, end = decoder.raw_decode(remaining)
    files.update({Path(f['path']).name: f for f in report['files']})
    remaining = remaining[end:].lstrip()
for case in cases:
    findings = files[case['path']].get('traits', [])
    ids = {t['id'] for t in findings}
    assert set(case.get('required', [])) <= ids, (case['path'], 'missing', ids)
    assert not set(case.get('forbidden', [])) & ids, (case['path'], 'forbidden', ids)
    assert not any(t['crit'] == 5 for t in findings), (case['path'], 'hostile')
    assert sum(t['crit'] == 4 for t in findings) <= case['max_suspicious'], case['path']
    print('PASS', case['path'])
