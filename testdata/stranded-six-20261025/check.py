#!/usr/bin/env python3
"""Exercise static naming controls; no fixture program is executed."""
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RULE = ('objectives/anti-static/obfuscation/name-mangling/function-name'
        '::applescript-long-decimal-handler-names')
CASES = {'numeric-handlers.applescript': True,
         'seven-numeric-handlers.applescript': False,
         'readable-handlers.applescript': False,
         'numeric-calls.applescript': False}
result = subprocess.run(
    [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
     '--format', 'json'] + [str(HERE / name) for name in CASES],
    capture_output=True, text=True, check=True)
assert not result.stderr.strip(), result.stderr
remaining = result.stdout
checked = 0
while remaining.strip():
    report, end = json.JSONDecoder().raw_decode(remaining.lstrip())
    remaining = remaining.lstrip()[end:]
    for item in report['files']:
        name = Path(item['path']).name
        if name in CASES:
            found = {trait['id'] for trait in item.get('traits', [])}
            assert (RULE in found) == CASES[name], (name, found)
            checked += 1
assert checked == len(CASES), checked
print(f'{checked} naming controls passed')
