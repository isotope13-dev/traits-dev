#!/usr/bin/env python3
"""Check linked download, offline credential and session-call boundaries."""
import argparse
import json
from pathlib import Path
import subprocess

here = Path(__file__).resolve().parent
root = here.parent.parent
parser = argparse.ArgumentParser()
parser.add_argument('--report', type=Path, help='Check an existing Cleave JSON report')
args = parser.parse_args()
if args.report:
    source = args.report.read_text()
else:
    source = subprocess.check_output([
        'cleave', '--traits-dir', str(root), '--format', 'jsonl',
        str(here / 'fixtures'),
    ], text=True)
# Both JSONL and older concatenated JSON report streams are accepted.
decoder = json.JSONDecoder()
results = {}
while source.strip():
    source = source.lstrip()
    report, consumed = decoder.raw_decode(source)
    source = source[consumed:]
    for file in report['files']:
        results[Path(file['path']).name] = {t['id'] for t in file.get('traits', [])}
for case in json.loads((here / 'cases.json').read_text()):
    actual = results[case['file']]
    missing = set(case['present']) - actual
    unwanted = set(case['absent']) & actual
    assert not missing and not unwanted, (case['file'], missing, unwanted)
    print('PASS', case['file'])
