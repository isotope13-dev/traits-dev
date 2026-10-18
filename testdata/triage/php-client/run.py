#!/usr/bin/env python3
"""Focused positive and near-miss controls for HTML/PHP carrier traits."""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
CASES = json.loads(Path(__file__).with_name('cases.json').read_text())

def check(case):
    result = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
         '--format', 'json', str(ROOT / case['path'])],
        capture_output=True, text=True)
    assert result.returncode in (0, 1), result.stderr
    assert result.stdout.strip(), result.stderr
    report = json.loads(result.stdout)
    found = {trait['id'] for file in report['files'] for trait in file['traits']}
    missing = set(case.get('matched', [])) - found
    unexpected = set(case.get('not_matched', [])) & found
    assert not missing and not unexpected, (case['path'], missing, unexpected)
    # Transparent OR composites are evaluated for consumers but can be
    # intentionally omitted from ordinary rendered findings.
    for trait in case.get('evaluated_matched', []):
        debug = subprocess.run(
            [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
             'test-rules', str(ROOT / case['path']), '--rules', trait],
            capture_output=True, text=True, check=True)
        assert '\nMATCHED ' + trait + ' (composite)' in debug.stdout, debug.stdout
    return case['path']

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    for path in pool.map(check, CASES['fixtures']):
        print('PASS', path)
