#!/usr/bin/env python3
"""Focused controls for conditional PHP writes and endpoint-like literals."""
import concurrent.futures
import json
import os
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
SPEC = json.loads((HERE / 'cases.json').read_text())


def check(case):
    result = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
         'test-rules', str(ROOT / case['path']), '--rules', ','.join(SPEC['rules'])],
        capture_output=True, text=True, timeout=240,
    )
    matched = set(re.findall(r'^MATCHED (\S+)', result.stdout, re.MULTILINE))
    expected = set(case['matched'])
    if result.returncode or matched != expected:
        raise AssertionError(f"{case['path']}: expected {expected}, got {matched}\n"
                             f"{result.stdout}\n{result.stderr}")
    return {'path': case['path'], 'matched': sorted(matched), 'passed': True}


if __name__ == '__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(check, SPEC['cases']))
    (HERE / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
    print(f'{len(results)} focused controls passed')
