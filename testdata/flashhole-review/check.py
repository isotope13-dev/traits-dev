#!/usr/bin/env python3
"""Check FlashHole positives and capability/intent boundaries with cleave."""
import json
import os
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[2]
cases = json.loads(Path(__file__).with_name('cases.json').read_text())
sources = json.loads(Path(__file__).with_name('fixture-sources.json').read_text())
fixture_root = Path('/usr/local/var/cyclotron/cleave/tests/fixtures/flashhole')
fixture_root.mkdir(parents=True, exist_ok=True)
for name, source in sources.items():
    (fixture_root / name).write_text(source)
command = [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(root), '--format', 'jsonl']
result = subprocess.run(command + [c['path'] for c in cases], cwd=root, text=True,
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
if result.returncode:
    sys.stderr.write(result.stderr)
    raise SystemExit(result.returncode)
reports = [json.loads(line) for line in result.stdout.splitlines() if line.strip()]
files = {str(Path(f['path']).resolve()): f
         for report in reports for f in report.get('files', [report])}
failures = []
for case in cases:
    path = (root / case['path']).resolve()
    file = files.get(str(path))
    if file is None:
        failures.append(f'{path.name}: missing analysis')
        continue
    ids = {t['id'] for t in file.get('traits', [])}
    missing = set(case['required']) - ids
    unexpected = set(case['forbidden']) & ids
    hostile = sum(t['crit'] == 5 for t in file.get('traits', []))
    suspicious = sum(t['crit'] == 4 for t in file.get('traits', []))
    if (missing or unexpected or hostile < case.get('hostile_floor', 0)
            or hostile > case.get('max_hostile', 999)
            or suspicious > case.get('max_suspicious', 999)):
        failures.append(f'{path.name}: missing={sorted(missing)}, unexpected={sorted(unexpected)}, hostile={hostile}')
    else:
        print(f'PASS {path.name}')
if failures:
    raise SystemExit('\n'.join(failures))
print(f'{len(cases)} FlashHole cases passed')
