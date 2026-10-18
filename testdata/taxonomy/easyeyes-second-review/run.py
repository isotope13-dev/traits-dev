#!/usr/bin/env python3
"""Run controls outside test-named paths, so exclusions cannot hide regressions."""
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

root = Path(__file__).resolve().parents[3]
cases = json.loads(Path(__file__).with_name('cases.json').read_text())['fixtures']
with tempfile.TemporaryDirectory(prefix='.review-easyeyes-', dir=root) as tmp:
    paths = []
    for case in cases:
        dst = Path(tmp) / Path(case['path']).name
        shutil.copyfile(root / case['path'], dst)
        paths.append(str(dst))
    result = subprocess.run(['cleave', '--traits-dir', str(root), '--json', *paths],
                            capture_output=True, text=True, check=True)
    if result.stderr.strip():
        print(result.stderr.strip())
    findings = {}
    for line in result.stdout.splitlines():
        report = json.loads(line)
        for file in report.get('files', []):
            findings[Path(file['path']).name] = {t['id'] for t in file.get('traits', [])}
    # Debug evaluation also checks baseline traits and pure-OR composites
    # that the scan renderer intentionally strips from its output.
    from concurrent.futures import ThreadPoolExecutor
    def check(case):
        target = str(Path(tmp) / Path(case['path']).name)
        ids = case['matched'] + case['not_matched']
        debug = subprocess.run(['cleave', '--traits-dir', str(root), 'test-rules',
                                target, '--rules', ','.join(ids)],
                               capture_output=True, text=True, check=True)
        actual = {line.split(' ', 2)[1] for line in debug.stdout.splitlines()
                  if line.startswith('MATCHED ')}
        missing = set(case['matched']) - actual
        unexpected = set(case['not_matched']) & actual
        return ({'case': case['case_id'], 'missing': sorted(missing),
                 'unexpected': sorted(unexpected)} if missing or unexpected else None)
    with ThreadPoolExecutor(max_workers=4) as pool:
        failures = [f for f in pool.map(check, cases) if f]
    if failures:
        raise SystemExit(json.dumps(failures, indent=2))
    print(f"{len(cases)} focused controls passed")
