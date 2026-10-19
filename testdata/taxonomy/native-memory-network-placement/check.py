#!/usr/bin/env python3
"""Check emitted capability IDs without executing any fixture code."""
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def main():
    cases = json.loads((HERE / 'cases.json').read_text())
    checks = 0
    for case in cases['fixtures']:
        result = subprocess.run(
            [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
             '--format', 'json', str(ROOT / case['path'])],
            check=True, capture_output=True, text=True)
        observed = {trait['id']: trait for file in json.loads(result.stdout)['files']
                    for trait in file.get('traits', [])}
        for trait in case.get('required_emitted', []):
            assert trait in observed, (case['path'], 'missing', trait)
            assert observed[trait]['crit'] == 3, (case['path'], trait, observed[trait])
            checks += 2
        for trait in case.get('forbidden_emitted', []):
            assert trait not in observed, (case['path'], 'unexpected', trait)
            checks += 1
        assert not [t for t in observed.values() if t['crit'] >= 4], case['path']
        checks += 1
    print(f'{checks} assertions passed across {len(cases["fixtures"])} source controls')


if __name__ == '__main__':
    main()
