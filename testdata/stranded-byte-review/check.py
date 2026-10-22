#!/usr/bin/env python3
"""Check source bindings statically; never import or execute the fixtures."""
import argparse
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    if args.report:
        output = args.report.read_text()
    else:
        run = subprocess.run(
            [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
             '--format', 'json'] +
            [str(HERE / case['path']) for case in json.loads((HERE / 'cases.json').read_text())],
            capture_output=True, text=True)
        assert run.returncode in (0, 1), run.stderr
        assert 'validation failed' not in run.stdout, run.stdout
        assert 'Warning:' not in run.stderr, run.stderr
        output = run.stdout
    decoder = json.JSONDecoder()
    findings = {}
    while output.strip():
        report, end = decoder.raw_decode(output.lstrip())
        output = output.lstrip()[end:]
        for file in report['files']:
            findings[Path(file['path']).name] = {
                trait['id']: trait['crit'] for trait in file.get('traits', [])}
    count = 0
    for case in json.loads((HERE / 'cases.json').read_text()):
        actual = findings[case['file']]
        for trait in case['present']:
            assert actual.get(trait) == 5, (case['file'], trait, actual)
            count += 1
        for trait in case['absent']:
            assert trait not in actual, (case['file'], trait, actual)
            count += 1
    print(f'{count} assertions passed across {len(json.loads((HERE / "cases.json").read_text()))} binding controls')


if __name__ == '__main__':
    main()
