"""Check emitted findings against the focused positive and near-miss cases."""
import concurrent.futures
import json
import os
import re
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[3]
cases = json.loads(Path(__file__).with_name('cases.json').read_text())['fixtures']

def check(case):
    result = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--no-update-check', '--traits-dir', str(root), '--format', 'json', str(root / case['path'])], capture_output=True, text=True)
    if result.returncode:
        return case['path'], [result.stderr or result.stdout]
    report = json.loads(result.stdout)
    found = {trait['id'] for file in report['files'] for trait in file.get('traits', [])}
    errors = ['missing ' + id for id in case.get('required_emitted', []) if id not in found]
    errors += ['unexpected ' + id for id in case.get('forbidden_emitted', []) if any(trait == id or (id.endswith('/') and trait.startswith(id)) for trait in found)]
    debug_ids = [id for id in case.get('matched', []) if id not in found]
    if debug_ids:
        debug = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--no-update-check', '--traits-dir', str(root), 'test-rules', '--rules', ','.join(debug_ids), str(root / case['path'])], capture_output=True, text=True)
        matched = set(re.findall(r'^MATCHED (\S+)', debug.stdout, re.MULTILINE))
        errors += ['did not match ' + id for id in debug_ids if id not in matched]
    return case['path'], errors

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    results = list(pool.map(check, cases))
for path, errors in results:
    print(('FAIL' if errors else 'PASS') + ' ' + path)
    for error in errors:
        print('  ' + error)
raise SystemExit(any(errors for _, errors in results))
