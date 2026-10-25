#!/usr/bin/env python3
"""Check retained capabilities, relocated references, and task-agent cleanup."""
import argparse
import json
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--report', type=Path)
args = parser.parse_args()
here = Path(__file__).resolve().parent
root = here.parents[2]
if args.report:
    text = args.report.read_text()
else:
    text = subprocess.run(
        ['cleave', '--traits-dir', str(root), '--format', 'json',
         'analyze', str(here)], check=True, capture_output=True, text=True
    ).stdout
decoder = json.JSONDecoder()
files = {}
while text.strip():
    report, end = decoder.raw_decode(text.lstrip())
    text = text.lstrip()[end:]
    for item in report['files']:
        files[Path(item['path']).name] = {
            t['id']: t['crit'] for t in item.get('traits', [])}
checks = 0
for name, case in json.loads((here / 'cases.json').read_text()).items():
    actual = files[name]
    for trait, severity in case.get('required', {}).items():
        assert actual.get(trait) == severity, (name, trait, actual.get(trait))
        checks += 1
    for trait in case.get('forbidden', []):
        assert trait not in actual, (name, trait)
        checks += 1
print(f'{checks} assertions passed across 12 controls')
