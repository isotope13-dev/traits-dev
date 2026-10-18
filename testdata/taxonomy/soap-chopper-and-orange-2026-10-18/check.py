#!/usr/bin/env python3
"""Check focused positive and near-miss fixtures without executing their code."""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[3]
cases = json.loads(Path(__file__).with_name('cases.json').read_text())['fixtures']

def check(case):
    command = [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(root), '--format', 'json', str(root / case['path'])]
    result = subprocess.run(command, text=True, capture_output=True, check=True)
    report = json.loads(result.stdout)
    emitted = {trait['id'] for file in report['files'] for trait in file['traits']}
    missing = set(case['required_emitted']) - emitted
    forbidden = set(case['forbidden_emitted']) & emitted
    assert not missing and not forbidden, (case['path'], sorted(missing), sorted(forbidden))
    return case['path']

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    for name in pool.map(check, cases):
        print('PASS', name, flush=True)
print(f'{len(cases)} focused cases passed')
