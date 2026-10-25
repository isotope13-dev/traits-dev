"""Scan inert controls from neutral paths; never execute their contents."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).parent
CASES = json.loads((HERE / 'cases.json').read_text())['fixtures']


def main():
    scratch = Path(sys.argv[1]).resolve()
    scratch.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='registry-controls-', dir=scratch) as tmp:
        staged = []
        for case in CASES:
            path = Path(tmp) / case['path']
            shutil.copyfile(HERE / case['path'], path)
            staged.append(str(path))
        result = subprocess.run(
            [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
             '--format', 'json', *staged], capture_output=True, text=True, check=True)
        decoder = json.JSONDecoder()
        source = result.stdout
        reports = {}
        while source.strip():
            item, end = decoder.raw_decode(source.lstrip())
            source = source.lstrip()[end:]
            for file in item.get('files', []):
                reports[file['path']] = {t['id'] for t in file.get('traits', [])}
        failures = []
        for case, path in zip(CASES, staged):
            if path not in reports:
                failures.append({'path': case['path'], 'error': 'missing report'})
                continue
            matches = reports[path]
            missing = set(case['matched']) - matches
            unexpected = set(case['not_matched']) & matches
            if missing or unexpected:
                failures.append({'path': case['path'], 'missing': sorted(missing),
                                 'unexpected': sorted(unexpected)})
    print(json.dumps({'cases': len(CASES), 'failures': failures}, indent=2))
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    return bool(failures)


if __name__ == '__main__':
    sys.exit(main())
