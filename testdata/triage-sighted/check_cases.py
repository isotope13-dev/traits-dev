"""Scan triage-sighted fixtures and verify declared findings.

Fixtures live under testdata/, whose path segments trip the taxonomy's own
test-harness suppressions (test-directory markers, harness contexts). Those
exclusions exist to keep real test suites from incriminating themselves; the
positive fixtures here are synthetic malware shapes that must be evaluated
as if in the wild. The runner therefore scans byte-identical copies staged
under a neutral temp directory (basenames preserved, so filename-pattern
exclusions still apply honestly) and compares trait IDs.
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CASES = json.loads((Path(__file__).parent / 'cases.json').read_text())['fixtures']

GENERATED = {'spy-hidden-imports.exe', 'self-upload.exe', 'plain.exe'}


def main() -> int:
    missing_build = [g for g in GENERATED
                     if not (Path(__file__).parent / g).exists()]
    if missing_build:
        print('missing generated fixtures (run build_pe_fixtures.py): '
              + ', '.join(missing_build))
        return 2
    with tempfile.TemporaryDirectory(prefix='triage-sighted-') as tmp:
        staged = []
        for case in CASES:
            src = ROOT / case['path']
            dst = Path(tmp) / Path(case['path']).name
            shutil.copyfile(src, dst)
            staged.append(str(dst))
        result = subprocess.run(
            ['cleave', '--traits-dir', str(ROOT), '--format', 'json', *staged],
            capture_output=True, text=True, check=True, cwd=ROOT)
        if result.stderr.strip():
            print(result.stderr)
        reports = {}
        decoder = json.JSONDecoder()
        source = result.stdout
        while source.strip():
            item, end = decoder.raw_decode(source.lstrip())
            source = source.lstrip()[end:]
            for file in item.get('files', []):
                reports[Path(file['path']).name] = {
                    trait['id'] for trait in file.get('traits', [])}
    failed = []
    for case in CASES:
        name = Path(case['path']).name
        matches = reports.get(name)
        if matches is None:
            failed.append({'path': case['path'], 'error': 'missing report'})
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
