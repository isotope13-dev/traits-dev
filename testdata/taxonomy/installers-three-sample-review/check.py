#!/usr/bin/env python3
"""Static fixture assertions; never run the scripts being analyzed."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cleave', default='cleave')
    args = parser.parse_args()
    cases = json.loads((HERE / 'cases.json').read_text())['fixtures']
    with tempfile.TemporaryDirectory() as temp:
        fixtures = Path(temp)
        for index, case in enumerate(cases):
            source = ROOT / case['path']
            case['basename'] = f'{index}/{source.name}'
            (fixtures / str(index)).mkdir()
            (fixtures / case['basename']).write_bytes(source.read_bytes())
        result = subprocess.run([args.cleave, '--traits-dir', str(ROOT), '--format', 'json',
                                 'analyze', str(fixtures)], text=True, capture_output=True)
    if result.returncode:
        raise SystemExit(result.stderr)
    reports = []
    remaining = result.stdout.lstrip()
    decoder = json.JSONDecoder()
    while remaining:
        report, end = decoder.raw_decode(remaining)
        reports.append(report)
        remaining = remaining[end:].lstrip()
    actual = {'/'.join(Path(file['path']).parts[-2:]): {trait['id'] for trait in file.get('traits', [])}
              for report in reports for file in report['files']}
    failures = []
    for case in cases:
        observed = actual.get(case['basename'], set())
        missing = sorted(set(case['matched']) - observed)
        unexpected = sorted(set(case['not_matched']) & observed)
        if missing or unexpected:
            failures.append(dict(case=case['case_id'], missing=missing, unexpected=unexpected))
    if failures:
        raise SystemExit(json.dumps(failures, indent=2))
    print(f'{len(cases)} static controls passed')


if __name__ == '__main__':
    main()
