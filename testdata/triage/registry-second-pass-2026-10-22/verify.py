#!/usr/bin/env python3
"""Scan the static controls without executing their contents."""
import argparse
import json
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[3]
parser = argparse.ArgumentParser()
parser.add_argument('--cleave', default='cleave')
parser.add_argument('--report', type=Path)
args = parser.parse_args()
cases = json.loads(Path(__file__).with_name('cases.json').read_text())['fixtures']
if args.report:
    output = args.report.read_text()
else:
    output = subprocess.check_output(
        [args.cleave, '--traits-dir', str(root), '--format', 'json',
         *[str(root / c['path']) for c in cases]], text=True)
reports = {}
decoder = json.JSONDecoder()
while output.strip():
    report, length = decoder.raw_decode(output.lstrip())
    output = output.lstrip()[length:]
    for file in report['files']:
        reports[Path(file['path']).name] = {t['id']: t for t in file.get('traits', [])}
for case in cases:
    traits = reports[Path(case['path']).name]
    for trait in case['required_emitted']:
        assert trait in traits, (case['case_id'], 'missing', trait)
    for trait in case['forbidden_emitted']:
        assert trait not in traits, (case['case_id'], 'unexpected', trait)
    for trait, finding in traits.items():
        if trait.startswith('micro-behaviors/communications/') and 'lnk-arg-' in trait:
            assert finding['crit'] == 3, (case['case_id'], 'reference criticality', trait)
print(f'{len(cases)} static positive/near-miss controls passed')
