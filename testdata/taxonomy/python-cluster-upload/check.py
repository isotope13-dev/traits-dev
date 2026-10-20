"""Scan the fixture sources; never execute collector code."""
import json
import os
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[3]
cases = json.loads((Path(__file__).with_name('cases.json')).read_text())['fixtures']
result = subprocess.run(
    [os.environ.get('CLEAVE', 'cleave'), '--json', *[c['path'] for c in cases]],
    cwd=root, capture_output=True, text=True, check=True,
)
reports = {
    f['path']: f
    for line in result.stdout.splitlines() if line.strip()
    for f in json.loads(line)['files']
}
errors = []
for case in cases:
    ids = {t['id'] for t in reports[case['path']].get('traits', [])}
    missing = set(case['matched']) - ids
    unexpected = set(case['not_matched']) & ids
    if missing or unexpected:
        errors.append((case['path'], sorted(missing), sorted(unexpected)))
assert not errors, errors
print(f"{len(cases)} source-to-send controls passed")
