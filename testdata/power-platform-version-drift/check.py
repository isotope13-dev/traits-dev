#!/usr/bin/env python3
"""Verify neutral construction evidence, near misses, and F5 exploit retention."""
import argparse
import json
import pathlib
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
root = pathlib.Path(__file__).resolve().parents[2]
cases = json.loads((pathlib.Path(__file__).parent / 'cases.json').read_text())['fixtures']
for case in cases:
    command = [args.cleave, '--traits-dir', str(root), '--format', 'json', str(root / case['path'])]
    result = subprocess.run(command, text=True, capture_output=True, check=True)
    report = json.loads(result.stdout)
    artifact = report['files'][0]
    found = {trait['id'] for trait in artifact.get('traits', [])}
    missing = set(case['matched']) - found
    unwanted = set(case['not_matched']) & found
    assert not missing and not unwanted, (case['path'], missing, unwanted)
    if case['path'].startswith('testdata/power-platform-version-drift/'):
        threats = [t['id'] for t in artifact.get('traits', []) if t['crit'] >= 4]
        assert not threats, (case['path'], threats)
    print('PASS', case['path'])
print(f'{len(cases)} controls passed')
