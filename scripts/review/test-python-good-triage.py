#!/usr/bin/env python3
"""Static endpoint-triage regressions: attack code, inert data, and ordinary software."""
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import shlex
import subprocess

ROOT = Path(__file__).resolve().parents[2]
TRAITS = Path(os.environ.get('TRAITS_DIR', ROOT))
ENGINE = shlex.split(os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave')))
CASES = [(label, path) for label in ('notable', 'suspicious', 'hostile')
         for path in sorted((ROOT / 'testdata' / label / 'generated/python-good-triage').iterdir())
         if path.is_file()]
CASES += [('hostile', ROOT / 'testdata/hostile/generated/tor-public-nonce' / name)
          for name in ('signature_recovery.py', 'precomputed_nonce_recovery.py')]
assert len(CASES) == 29, 'A focused fixture is missing'

def scan(case):
    label, path = case
    result = subprocess.run([*ENGINE, '--traits-dir', str(TRAITS), '--format', 'json', str(path)],
                            capture_output=True, text=True, check=True)
    report = json.loads(result.stdout)['files'][0]
    high = [trait for trait in report.get('traits', []) if trait['crit'] >= 4]
    hostile = {trait['id'].split('::')[0] for trait in high if trait['crit'] == 5}
    if label == 'hostile':
        assert len(hostile) >= 2, (path.name, 'Needs two hostile directories', [t['id'] for t in high])
    elif label == 'suspicious':
        assert len(high) == 1 and high[0]['crit'] == 4, (path.name, high)
    else:
        assert not high, (path.name, [t['id'] for t in high])
    return path.name

with ThreadPoolExecutor(max_workers=4) as workers:
    passed = list(workers.map(scan, CASES))
print(f'Python good-pool regressions: {len(passed)} static fixtures passed')
