#!/usr/bin/env python3
"""Check real samples and focused near misses with one Cleave invocation."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
parser = argparse.ArgumentParser()
parser.add_argument('--cleave', default='cleave')
parser.add_argument('--report', type=Path, help='Reuse an existing full JSON report')
args = parser.parse_args()
cases = json.loads((HERE / 'cases.json').read_text())['cases']
originals = json.loads((HERE / 'provenance.json').read_text())['originals']
for name, expected in originals.items():
    assert hashlib.sha256((HERE / name).read_bytes()).hexdigest() == expected, name
if args.report:
    text = args.report.read_text()
else:
    command = [args.cleave, '--traits-dir', str(ROOT), '--format', 'json']
    command.extend(str(HERE / case['file']) for case in cases)
    text = subprocess.check_output(command, cwd=ROOT, text=True)
reports = {}
while text.strip():
    report, end = json.JSONDecoder().raw_decode(text.lstrip())
    text = text.lstrip()[end:]
    for file in report.get('files', [report]):
        reports[Path(file['path']).name] = {trait['id'] for trait in file.get('traits', [])}
failures = []
for case in cases:
    name = case['file']
    assert name in reports, f'Unanalyzed fixture: {name}'
    for trait in case.get('present', []):
        if trait not in reports[name]:
            failures.append(f'{name}: missing {trait}')
    for trait in case.get('absent', []):
        if trait in reports[name]:
            failures.append(f'{name}: unexpected {trait}')
assert not failures, '\n'.join(failures)
print(f'{len(cases)} focused cases passed; original hashes verified')
