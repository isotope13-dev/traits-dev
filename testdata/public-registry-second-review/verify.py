"""Static positive and near-miss controls; never executes fixture contents."""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def check(case):
    result = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
         '--format', 'json', str(HERE / case['path'])],
        env=dict(os.environ, CLEAVE_VALIDATE='0'),
        text=True, capture_output=True, check=True)
    report = json.loads(result.stdout)
    traits = {t['id']: t for f in report['files'] for t in f.get('traits', [])}
    missing = set(case['required']) - traits.keys()
    false = set(case['forbidden']) & traits.keys()
    assert not missing and not false, (case['path'], missing, false)
    for key, criticality in [('max_hostile', 5), ('max_suspicious', 4)]:
        cap = case.get(key)
        if cap is not None:
            found = [id for id, t in traits.items() if t['crit'] == criticality]
            assert len(found) <= cap, (case['path'], key, found)
    return 'PASS ' + case['path']


if __name__ == '__main__':
    cases = json.loads((HERE / 'cases.json').read_text())
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(check, case) for case in cases]
        failures = []
        for future in futures:
            try:
                print(future.result(), flush=True)
            except Exception as exc:
                failures.append(str(exc))
                print('FAIL', exc, flush=True)
        assert not failures, failures
