#!/usr/bin/env python3
"""Verify the instruction relationships and typed-FFI boundaries in saved scans."""
import argparse
import json
from pathlib import Path
import subprocess

here = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--report', type=Path)
args = parser.parse_args()
source = args.report.read_text() if args.report else subprocess.check_output(
    ['cleave', '--traits-dir', str(here.parent.parent), '--format', 'jsonl',
     '--all-files', str(here)], text=True)
decoder = json.JSONDecoder()
results = {}
while source.strip():
    report, used = decoder.raw_decode(source.lstrip())
    source = source.lstrip()[used:]
    for file in report.get('raw', report)['files']:
        name = Path(file['path'].split('!!')[-1]).name
        if name.endswith('.dat') and '!!' not in file['path']:
            continue  # These controls are intentionally analyzed as archive data.
        results[name] = {t['id'] for t in file.get('traits', [])}
for case in json.loads((here / 'cases.json').read_text()):
    actual = results[case['file']]
    missing = set(case['present']) - actual
    unwanted = set(case['absent']) & actual
    assert not missing and not unwanted, (case['file'], missing, unwanted)
    print('PASS', case['file'])
