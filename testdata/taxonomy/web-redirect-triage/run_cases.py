#!/usr/bin/env python3
"""Check HTML behavioral boundaries; optionally reuse a saved cleave report."""
import argparse
import json
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cleave', default='cleave')
parser.add_argument('--report', type=Path)
args = parser.parse_args()
root = Path(__file__).resolve().parents[3]
cases_path = Path(__file__).with_name('cases.json')
cases = json.loads(cases_path.read_text())['fixtures']
if args.report:
    source = args.report.read_text()
else:
    result = subprocess.run(
        [args.cleave, '--traits-dir', str(root), '--format', 'json',
         str(cases_path.parent)], text=True, capture_output=True, check=True)
    source = result.stdout
    if result.stderr:
        print(result.stderr, end='')
# The streaming json renderer can concatenate complete report objects.
decoder = json.JSONDecoder()
files = {}
while source.strip():
    source = source.lstrip()
    report, end = decoder.raw_decode(source)
    source = source[end:]
    for item in report.get('files', [report]):
        files[Path(item['path']).name] = item
failures = []
for case in cases:
    filename = Path(case['path']).name
    assert filename in files, 'Missing scanned fixture: ' + filename
    traits = {t['id']: t for t in files[filename].get('traits', [])}
    errors = [t + ' missing' for t in case['matched'] if t not in traits]
    errors += [t + ' unexpected' for t in case['not_matched'] if t in traits]
    errors += [t + ' wrong criticality' for t, level in
               case['criticalities'].items() if traits.get(t, {}).get('crit') != level]
    if errors:
        failures.append((filename, errors))
    print(filename + ': ' + ('; '.join(errors) if errors else 'PASS'))
assert not failures, failures
print(str(len(cases)) + ' boundary controls passed')
