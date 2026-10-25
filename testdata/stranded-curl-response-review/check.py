#!/usr/bin/env python3
"""Check static output-capture observations without executing fixture code."""
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RULE = ('micro-behaviors/communications/http/client/response-body'
        '::applescript-curl-http-output-assignment')
POSITIVE = {'capture.applescript', 'parenthesized.applescript',
            'escaped.applescript', 'show-errors.applescript'}
paths = sorted(HERE.glob('*.applescript'))
result = subprocess.run(
    [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
     '--format', 'json', *map(str, paths)],
    capture_output=True, text=True, check=True)
assert not result.stderr.strip(), result.stderr
remaining = result.stdout
checked = set()
while remaining.strip():
    report, end = json.JSONDecoder().raw_decode(remaining.lstrip())
    remaining = remaining.lstrip()[end:]
    for item in report['files']:
        name = Path(item['path']).name
        found = {trait['id'] for trait in item.get('traits', [])}
        assert (RULE in found) == (name in POSITIVE), (name, found)
        checked.add(name)
assert checked == {p.name for p in paths}, checked
print(f'{len(checked)} static output-capture controls passed')
