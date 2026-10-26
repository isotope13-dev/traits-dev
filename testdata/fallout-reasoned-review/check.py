#!/usr/bin/env python3
"""Static positive/near-miss checks; none of the fixtures is executed."""
import json
import os
from pathlib import Path
import subprocess
import shutil
import tempfile

HERE = Path(__file__).resolve().parent
cases = json.loads((HERE / 'cases.json').read_text())
with tempfile.TemporaryDirectory(prefix='.fallout-controls-', dir=HERE.parents[1]) as staging:
    # Keep test-directory exclusions from deciding behavior-only controls.
    paths = []
    for index, case in enumerate(cases):
        target = Path(staging) / f'{index}-{Path(case["path"]).name}'
        shutil.copyfile(HERE / case['path'], target)
        paths.append(str(target))
    result = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--format', 'jsonl', *paths],
        text=True, capture_output=True, check=True,
    )
reports = {}
for line in result.stdout.splitlines():
    report = json.loads(line)
    for file in report['files']:
        reports[file['path']] = {trait['id'] for trait in file.get('traits', [])}
failures = []
for case, path in zip(cases, paths):
    observed = reports.get(path, set())
    for trait in case['present']:
        if trait not in observed:
            failures.append(f'{case["path"]}: missing {trait}')
    for trait in case['absent']:
        if trait in observed:
            failures.append(f'{case["path"]}: unexpected {trait}')
if failures:
    raise SystemExit('\n'.join(failures))
print(f'{len(cases)} static positive/near-miss controls passed')
