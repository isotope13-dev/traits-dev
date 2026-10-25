#!/usr/bin/env python3
"""Static assertions; compiled controls and analyzed scripts are never run."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cleave', default='cleave')
    parser.add_argument('--go', default='go')
    args = parser.parse_args()
    cases = json.loads((HERE / 'cases.json').read_text())['fixtures']
    with tempfile.TemporaryDirectory() as temp:
        fixtures = Path(temp)
        for index, case in enumerate(cases):
            source = ROOT / case['path']
            case['basename'] = f'{index}/{source.name}'
            (fixtures / str(index)).mkdir()
            (fixtures / case['basename']).write_bytes(source.read_bytes())
        chmod_ids = ['micro-behaviors/fs/chmod/modify::go-os-chmod-binary',
                     'micro-behaviors/fs/chmod/modify::go-file-chmod-binary']
        for name, positive in [('go-permission-write', True), ('go-no-fs', False)]:
            relative = f'{name}/control.elf'
            target = fixtures / relative
            target.parent.mkdir()
            build = subprocess.run(
                [args.go, 'build', '-trimpath', '-buildvcs=false', '-ldflags', '-s -w',
                 '-o', str(target), str(HERE / f'{name}.go')],
                env={**os.environ, 'CGO_ENABLED': '0', 'GOOS': 'linux',
                     'GOARCH': 'amd64', 'GOTOOLCHAIN': 'local'},
                text=True, capture_output=True)
            if build.returncode:
                raise SystemExit(build.stderr)
            cases.append(dict(case_id=name, basename=relative,
                              matched=chmod_ids if positive else [],
                              not_matched=[] if positive else chmod_ids))
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
