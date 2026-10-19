#!/usr/bin/env python3
"""Check evidence boundaries without executing any fixture code."""
import json
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[3]
cases = json.loads(Path(__file__).with_name('cases.json').read_text())['fixtures']
cmd = [sys.argv[1] if len(sys.argv) > 1 else 'cleave', '--traits-dir', str(root),
       '--format', 'json', *[str(root / c['path']) for c in cases]]
result = subprocess.run(cmd, cwd=root, text=True, capture_output=True)
if result.returncode or result.stderr.strip():
    raise SystemExit(result.stderr or result.stdout)
remaining = result.stdout.lstrip()
decoder = json.JSONDecoder()
observed = {}
while remaining:
    report, end = decoder.raw_decode(remaining)
    for file in report['files']:
        observed.setdefault(str(Path(file['path']).resolve()), set()).update(
            t['id'] for t in file.get('traits', []))
    remaining = remaining[end:].lstrip()
for case in cases:
    path = str((root / case['path']).resolve())
    assert path in observed, f'Unanalyzed fixture: {path}'
    actual = observed[path]
    missing = set(case['matched']) - actual
    unwanted = set(case['not_matched']) & actual
    assert not missing and not unwanted, (case['path'], missing, unwanted)
print(f'{len(cases)} evidence-boundary controls passed')
