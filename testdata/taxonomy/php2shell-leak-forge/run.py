#!/usr/bin/env python3
"""Run boundary fixtures from paths without test-directory suppressions."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

root = Path(__file__).resolve().parents[3]
cases = json.loads(Path(__file__).with_name('cases.json').read_text())['fixtures']
with tempfile.TemporaryDirectory(prefix='php2shell-leak-forge-') as staging:
    paths = {}
    for case in cases:
        source = root / case['path']
        target = Path(staging) / source.name
        shutil.copyfile(source, target)
        paths[str(target)] = case
    result = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(root), '--json', staging],
        env={**os.environ, 'CLEAVE_VALIDATE': '0'},
        capture_output=True, text=True, check=True,
    )
    seen = set()
    errors = []
    for line in result.stdout.splitlines():
        for report in json.loads(line).get('files', []):
            path = report['path']
            if path not in paths:
                continue
            seen.add(path)
            case = paths[path]
            ids = {t['id'] for t in report.get('traits', [])}
            missing = set(case['matched']) - ids
            unexpected = set(case['not_matched']) & ids
            if missing or unexpected:
                errors.append((case['path'], sorted(missing), sorted(unexpected)))
    assert seen == set(paths), f'missing reports: {set(paths) - seen}'
    assert not errors, f'(fixture, missing, unexpected): {errors}'
print(f'{len(cases)} boundary fixtures passed')
