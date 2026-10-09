"""Run focused trait controls outside paths that suppress test fixtures."""
import concurrent.futures
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CASES = json.loads((HERE / 'cases.json').read_text())
ENV = os.environ.copy()
ENV.pop('CLEAVE_VALIDATE', None)


def check(item):
    name, expected = item
    with tempfile.TemporaryDirectory(prefix='registry-review-', dir=os.environ.get('TRIAGE_SCRATCH')) as directory:
        target = Path(directory) / name
        shutil.copyfile(HERE / name, target)
        result = subprocess.run(
            ['cleave', '--traits-dir', str(ROOT), '--format', 'json',
             'analyze', str(target)],
            env=ENV, capture_output=True, text=True,
        )
    try:
        found = {trait['id'] for trait in json.loads(result.stdout)['files'][0]['traits']}
    except (ValueError, KeyError, IndexError):
        found = set()
    mismatches = [trait for trait, wanted in expected.items()
                  if (trait in found) != wanted]
    if result.returncode or mismatches:
        return name, False, 'Mismatched traits: ' + ', '.join(mismatches) + '\n' + result.stderr
    return name, True, ''


with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    results = list(pool.map(check, CASES.items()))
for name, passed, details in results:
    print(name + ': ' + ('PASS' if passed else 'FAIL'))
    if details:
        print(details)
raise SystemExit(0 if all(passed for _, passed, _ in results) else 1)
