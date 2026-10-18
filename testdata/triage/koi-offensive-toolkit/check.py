#!/usr/bin/env python3
"""Scan inert fixtures; never import or execute their payload generators."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def reports(text):
    decoder = json.JSONDecoder()
    while text.strip():
        text = text.lstrip()
        report, end = decoder.raw_decode(text)
        yield report
        text = text[end:]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cleave', default='cleave')
    args = parser.parse_args()
    cases = json.loads((HERE / 'cases.json').read_text())['fixtures']
    with tempfile.TemporaryDirectory(prefix='koi-controls-') as tmp:
        for case in cases:
            shutil.copyfile(HERE / case['file'], Path(tmp) / case['file'])
        result = subprocess.run(
            [args.cleave, '--no-update-check', '--traits-dir', str(ROOT),
             '--format', 'json', tmp],
            env={**os.environ, 'CLEAVE_SKIP_CACHE': '1'},
            text=True, capture_output=True, check=True,
        )
        found = {}
        for report in reports(result.stdout):
            for file in report['files']:
                found[Path(file['path']).name] = {
                    trait['id']: trait['crit'] for trait in file.get('traits', [])
                }
        failures = []
        for case in cases:
            traits = found[case['file']]
            for rule, criticality in case['required'].items():
                if traits.get(rule) != criticality:
                    failures.append(f"{case['file']}: expected {rule}={criticality}, got {traits.get(rule)}")
            for rule in case['forbidden']:
                if rule in traits:
                    failures.append(f"{case['file']}: unexpected {rule}={traits[rule]}")
        if failures:
            raise SystemExit('\n'.join(failures))
    print(f'PASS: {len(cases)} static positive and negative controls')


if __name__ == '__main__':
    main()
