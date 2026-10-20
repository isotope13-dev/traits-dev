#!/usr/bin/env python3
"""Exercise binding and context boundaries without executing sample code."""
import json
import os
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parent
repo = root.parents[1]
cases = json.loads((root / 'cases.json').read_text())
for case in cases:
    result = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(repo),
         '--json', str(root / case['path'])],
        capture_output=True, text=True, check=True)
    records = [json.loads(line) for line in result.stdout.splitlines() if line.strip()]
    def ids(node):
        if isinstance(node, dict):
            if 'id' in node and ('crit' in node or 'criticality' in node):
                yield node['id']
            for value in node.values():
                yield from ids(value)
        elif isinstance(node, list):
            for item in node:
                yield from ids(item)
    found = set(ids(records))
    missing = set(case['present']) - found
    unexpected = set(case['absent']) & found
    assert not missing and not unexpected, (case['path'], missing, unexpected)
    print('PASS', case['path'])
print(f'{len(cases)} focused cases passed')
