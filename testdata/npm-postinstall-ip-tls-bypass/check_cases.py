"""Focused regression cases for url-first https.get TLS-bypass detection.

No fixture code is executed; cleave only scans the files. Fixtures live
under testdata/, whose path segments trip the taxonomy's own test-harness
suppressions, so the runner stages byte-identical copies under a neutral
temp directory (basenames preserved, so filename-pattern exclusions still
apply honestly) and compares trait IDs on the staged paths.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).parent
CASES = json.loads((HERE / 'cases.json').read_text())['fixtures']

# Loose files staged for scanning; archives are staged whole and their
# members are addressed as <archive>!!<inner path> in cleave reports.
STAGED = [
    'dropper.tgz',
    'benign-registry.tgz',
    'url-first-bypass.js',
    'options-first-bypass.js',
    'loopback-bypass.js',
    'plain-get.js',
]

CLEAVE = os.environ.get('CLEAVE', 'cleave')


def staged_case_path(tmp, case_path):
    rel = Path(case_path).relative_to('testdata/npm-postinstall-ip-tls-bypass')
    return str(Path(tmp) / rel)


def main():
    with tempfile.TemporaryDirectory(prefix='npm-postinstall-ip-tls-bypass-') as tmp:
        for name in STAGED:
            shutil.copyfile(HERE / name, Path(tmp) / name)
        staged = [str(Path(tmp) / name) for name in STAGED]
        result = subprocess.run(
            [CLEAVE, '--traits-dir', str(ROOT), '--format', 'json', *staged],
            capture_output=True, text=True, check=True, cwd=str(ROOT))
        if result.stderr.strip():
            print(result.stderr)
        reports = {}
        decoder = json.JSONDecoder()
        source = result.stdout
        while source.strip():
            item, end = decoder.raw_decode(source.lstrip())
            source = source.lstrip()[end:]
            for file in item.get('files', []):
                reports[file['path']] = {
                    trait['id'] for trait in file.get('traits', [])}
    failed = []
    for case in CASES:
        key = staged_case_path(tmp, case['path'])
        matches = reports.get(key)
        if matches is None:
            failed.append({'path': case['path'], 'error': 'missing report',
                           'seen': sorted(reports)})
            continue
        missing = set(case.get('matched', [])) - matches
        unexpected = set(case.get('not_matched', [])) & matches
        if missing or unexpected:
            failed.append({'path': case['path'], 'missing': sorted(missing),
                           'unexpected': sorted(unexpected)})
    print(json.dumps({'cases': len(CASES), 'failures': failed}, indent=2))
    return bool(failed)


if __name__ == '__main__':
    sys.exit(main())
