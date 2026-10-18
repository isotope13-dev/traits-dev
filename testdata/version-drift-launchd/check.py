"""Check neutral launchd configuration and retained remote-code objectives."""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
CASES = json.loads(Path(__file__).with_name('cases.json').read_text())

def check(case):
    result = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
         '--format', 'json', str(ROOT / case['path'])],
        check=True, capture_output=True, text=True,
    )
    traits = json.loads(result.stdout)['files'][0].get('traits', [])
    ids = {t['id'] for t in traits}
    assert set(case['required']) <= ids, (case['path'], set(case['required']) - ids)
    assert not set(case['forbidden']) & ids, (case['path'], set(case['forbidden']) & ids)
    if case['max_suspicious'] is not None:
        assert not [t for t in traits if t['crit'] >= 4], (case['path'], traits)
    return case['path']

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    for path in pool.map(check, CASES):
        print('PASS', path)
