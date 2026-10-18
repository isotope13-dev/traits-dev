#!/usr/bin/env python3
"""Run precision controls outside test-directory suppression contexts."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cleave', default='cleave')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[3]
    cases = json.loads(Path(__file__).with_name('cases.json').read_text())['fixtures']
    with tempfile.TemporaryDirectory(prefix='.registry-control-', dir=root) as tmp:
        targets = []
        for case in cases:
            target = Path(tmp) / case['case_id']
            shutil.copyfile(root / case['path'], target)
            targets.append(str(target))
        result = subprocess.run(
            [args.cleave, '--traits-dir', str(root), '--json', *targets],
            capture_output=True, text=True, check=True,
        )
        files = [f for line in result.stdout.splitlines()
                 for f in json.loads(line).get('files', [])]
        failures = []
        for case in cases:
            ids = {t['id'] for f in files
                   if f.get('path') == str(Path(tmp) / case['case_id'])
                   for t in f.get('traits', [])}
            missing = sorted(set(case['matched']) - ids)
            unexpected = sorted(set(case['not_matched']) & ids)
            if missing or unexpected:
                failures.append(dict(case=case['case_id'], missing=missing,
                                     unexpected=unexpected))
        if failures:
            raise SystemExit(json.dumps(failures, indent=2))
        print(f'{len(cases)} precision controls passed')


if __name__ == '__main__':
    main()
