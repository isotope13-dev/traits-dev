"""Scan static controls; copy fixtures away from test-path exclusions."""
import argparse
import concurrent.futures
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('--filter', default='')
args = parser.parse_args()
case_file = Path(__file__).with_name('cases.json')
cases = json.loads(case_file.read_text())['fixtures']
cases = [c for c in cases if args.filter in c['path']]

def check(case):
    with tempfile.TemporaryDirectory(prefix='registry-control-') as temporary:
        target = Path(temporary) / Path(case['path']).name
        shutil.copyfile(case['path'], target)
        identifiers = case['matched'] + case['not_matched']
        result = subprocess.run(
            ['cleave', '--traits-dir', '.', 'test-rules', str(target),
             '--rules', ','.join(identifiers)], capture_output=True, text=True)
        output = result.stdout + result.stderr
        passed = result.returncode == 0 and 'validation failed' not in output
        for identifier in case['matched']:
            passed &= bool(re.search(r'^MATCHED ' + re.escape(identifier) + ' ', output, re.M))
        for identifier in case['not_matched']:
            passed &= bool(re.search(r'^NOT MATCHED ' + re.escape(identifier) + ' ', output, re.M))
        return case['path'], passed, output

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    results = list(pool.map(check, cases))
for path, passed, output in results:
    print(('PASS ' if passed else 'FAIL ') + path)
    if not passed:
        print(output)
raise SystemExit(0 if all(passed for _, passed, _ in results) else 1)
