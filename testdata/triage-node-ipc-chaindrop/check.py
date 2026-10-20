#!/usr/bin/env python3
"""Check positive and near-miss trait cases without executing fixture code."""
import concurrent.futures
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CASES = json.loads(Path(__file__).with_name('cases.json').read_text())['fixtures']

def check(case):
    rules = case['matched'] + case['not_matched']
    result = subprocess.run(
        ['cleave', '--traits-dir', '.', 'test-rules', case['path'],
         '--rules', ','.join(rules)], cwd=ROOT, capture_output=True, text=True)
    output = result.stdout + result.stderr
    problems = []
    for rule in case['matched']:
        if '\nMATCHED ' + rule + ' (' not in output:
            problems.append('missing ' + rule)
    for rule in case['not_matched']:
        if '\nMATCHED ' + rule + ' (' in output:
            problems.append('unexpected ' + rule)
    if result.returncode or 'validation failed' in output or 'Warning: Rule ' in output:
        problems.append('rule loading failed')
    return case['path'], problems, output

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    results = list(pool.map(check, CASES))
for path, problems, output in results:
    print(('FAIL ' if problems else 'PASS ') + path)
    if problems:
        print('\n'.join(problems))
        print(output)
raise SystemExit(any(problems for _, problems, _ in results))
