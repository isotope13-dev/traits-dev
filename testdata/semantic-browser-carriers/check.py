"""Run shuffled-carrier positives and missing-evidence near misses."""
import json
import os
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[2]
fixtures = json.loads(Path(__file__).with_name('cases.json').read_text())['fixtures']
paths = [str(root / item['path']) for item in fixtures]
proc = subprocess.run([sys.argv[1] if len(sys.argv) > 1 else 'cleave', '--format',
                       'jsonl', *paths], cwd=root, text=True, capture_output=True,
                      env={**os.environ, 'CLEAVE_SKIP_CACHE': '1'})
if proc.returncode:
    print(proc.stderr)
    raise SystemExit(proc.returncode)
reports = {}
for line in proc.stdout.splitlines():
    for file in json.loads(line)['files']:
        reports[Path(file['path']).name] = {trait['id'] for trait in file['traits']}
failures = []
for item in fixtures:
    ids = reports.get(Path(item['path']).name, set())
    missing = set(item['matched']) - ids
    unexpected = set(item['not_matched']) & ids
    if missing or unexpected:
        failures.append((item['path'], sorted(missing), sorted(unexpected)))
if failures:
    for path, missing, unexpected in failures:
        print(path, 'missing:', missing, 'unexpected:', unexpected)
    raise SystemExit(1)
print(f'{len(fixtures)} carrier controls passed')
