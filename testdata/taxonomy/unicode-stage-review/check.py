#!/usr/bin/env python3
"""Exercise escaped commands, code construction and Unicode decode boundaries."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cleave', default='cleave')
parser.add_argument('--scratch-root', required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parents[3]
fixtures = Path(__file__).resolve().parent
cases = json.loads((fixtures / 'cases.json').read_text())
with tempfile.TemporaryDirectory(prefix='stage-controls-', dir=args.scratch_root) as temp:
    def check(case):
        path = Path(temp) / case['file']
        shutil.copyfile(fixtures / case['file'], path)
        rules = case['matched'] + case['not_matched']
        result = subprocess.run(
            [args.cleave, '--no-update-check', '--traits-dir', str(root),
             'test-rules', str(path), '--rules', ','.join(rules)],
            text=True, capture_output=True, check=True)
        output = result.stdout + result.stderr
        for rule in case['matched']:
            assert any(line.startswith(f'MATCHED {rule} (') for line in output.splitlines()), output
        for rule in case['not_matched']:
            assert any(line.startswith(f'NOT MATCHED {rule} (') for line in output.splitlines()), output
        print('PASS', case['file'], flush=True)
    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(check, cases))
print(f'{len(cases)} controls passed')
