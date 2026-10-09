#!/usr/bin/env python3
"""Scan controls from neutral paths so production exclusions stay intact."""
import argparse
import concurrent.futures
import json
from pathlib import Path
import shutil
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--work-dir', type=Path, required=True)
parser.add_argument('--cleave', default='cleave')
parser.add_argument('--start', type=int, default=0)
parser.add_argument('--timeout', type=int, default=120)
args = parser.parse_args()
repo = Path(__file__).resolve().parents[3]
cases = json.loads(Path(__file__).with_name('cases.json').read_text())['fixtures'][args.start:]
args.work_dir.mkdir(parents=True, exist_ok=True)
for case in cases:
    shutil.copyfile(repo / case['path'], args.work_dir / Path(case['path']).name)

def check(case):
    rules = case['matched'] + case['not_matched']
    target = args.work_dir / Path(case['path']).name
    try:
        result = subprocess.run(
            [args.cleave, '--traits-dir', str(repo), 'test-rules', '--rules',
             ','.join(rules), str(target)], capture_output=True, text=True,
            timeout=args.timeout)
        output = result.stdout + result.stderr
        expected = {rule: True for rule in case['matched']}
        expected.update({rule: False for rule in case['not_matched']})
        actual = {rule: ('MATCHED ' + rule) in result.stdout and
                  ('NOT MATCHED ' + rule) not in result.stdout for rule in rules}
        passed = (result.returncode == 0 and expected == actual and
                  all(('MATCHED ' + rule) in result.stdout for rule in rules))
        (args.work_dir / (target.name + '.log')).write_text(output)
        record = {**case, 'actual': actual, 'passed': passed}
    except subprocess.TimeoutExpired:
        record = {**case, 'passed': False, 'error': 'scan timeout'}
    print(target.name, 'PASS' if record['passed'] else 'FAIL', flush=True)
    return record

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    records = list(executor.map(check, cases))
(args.work_dir / 'results.json').write_text(json.dumps(records, indent=2) + '\n')
raise SystemExit(0 if all(record['passed'] for record in records) else 1)
