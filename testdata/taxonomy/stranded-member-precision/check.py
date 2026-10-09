"""Check capability placement and benign near misses without executing samples."""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess

cases = json.loads(Path(__file__).with_name('cases.json').read_text())['fixtures']
env = os.environ.copy()
for key in ('SCAN_HOPPER', 'SCAN_REGISTRY_MAP', 'CLEAVE_VALIDATE'):
    env.pop(key, None)

def check(case):
    result = subprocess.run(
        ['atomscan', '--no-update', '--follow=none', '--mode', 'slow',
         '--format', 'json', case['path']], env=env, capture_output=True,
        text=True, check=True)
    report = json.loads(result.stdout.splitlines()[0])
    traits = report['raw']['files'][0]['traits']
    ids = {trait['id'] for trait in traits}
    assert set(case['matched']) <= ids, (case['path'], set(case['matched']) - ids)
    assert not set(case['not_matched']) & ids, (case['path'], set(case['not_matched']) & ids)
    assert not any(t['crit'] == 5 for t in traits), case['path']
    assert sum(t['crit'] == 4 for t in traits) <= 1, case['path']
    return case['path']

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    for path in pool.map(check, cases):
        print('PASS', path)
