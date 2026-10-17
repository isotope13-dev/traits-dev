#!/usr/bin/env python3
"""Exercise benign near misses for the credential-review rule changes."""
import concurrent.futures
import json
import os
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[3]
CASES = json.loads(Path(__file__).with_name('cases.json').read_text())['fixtures']

def check(case):
    expected = case['matched'] + case['not_matched']
    proc = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
         'test-rules', str(ROOT / case['path']), '--rules', ','.join(expected)],
        text=True, capture_output=True)
    actual = set(re.findall(r'^MATCHED (\S+)', proc.stdout, re.MULTILINE))
    missing = set(case['matched']) - actual
    unexpected = set(case['not_matched']) & actual
    if proc.returncode or missing or unexpected:
        return (case['case_id'], False, proc.stdout + proc.stderr)
    return (case['case_id'], True, '')

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(check, CASES))
for name, passed, details in results:
    print(('PASS' if passed else 'FAIL') + ' ' + name)
    if details:
        print(details)
raise SystemExit(not all(passed for _, passed, _ in results))
