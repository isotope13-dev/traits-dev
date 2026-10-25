#!/usr/bin/env python3
"""Run from the repository root; samples are parsed, never executed."""
import json
import os
from pathlib import Path
import subprocess
import sys

CASES = Path(__file__).with_name('cases.json')
cases = json.loads(CASES.read_text())['fixtures']
if len(sys.argv) > 1:
    output = Path(sys.argv[1]).read_text()
else:
    output = subprocess.check_output(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', '.', '--format',
         'json', *[case['path'] for case in cases]], text=True)
decoder = json.JSONDecoder()
files = {}
position = 0
while position < len(output):
    while position < len(output) and output[position].isspace():
        position += 1
    if position == len(output):
        break
    report, position = decoder.raw_decode(output, position)
    for item in report['files']:
        files[item['path']] = item
for case in cases:
    item = files[case['path']]
    present = {trait['id'] for trait in item.get('traits', [])}
    missing = set(case['matched']) - present
    unexpected = set(case['not_matched']) & present
    assert not missing and not unexpected, (case['path'], missing, unexpected)
    # Unreferenced baseline composites can be omitted from serialized output;
    # inspect rule evaluation when a case explicitly asks for that check.
    for key, prefix in [('debug_matched', 'MATCHED '),
                        ('debug_not_matched', 'NOT MATCHED ')]:
        for trait in case.get(key, []):
            debug = subprocess.check_output(
                [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', '.',
                 'test-rules', case['path'], '--rules', trait], text=True)
            assert '\n' + prefix + trait + ' ' in debug, debug
print(f'{len(cases)} focused capability and retained-attack controls passed')
