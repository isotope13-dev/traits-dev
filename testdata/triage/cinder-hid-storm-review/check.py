#!/usr/bin/env python3
"""Check passive token-format fixtures without executing their contents."""
import json
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[3]
fixtures = Path(__file__).resolve().parent
result = subprocess.run(
    [sys.argv[1] if len(sys.argv) > 1 else 'cleave', '--traits-dir', str(root),
     '--json', str(fixtures / 'token-pattern-only.py'),
     str(fixtures / 'store-paths-only.py')],
    capture_output=True, text=True, check=True,
)
reports = [f for line in result.stdout.splitlines()
           for f in json.loads(line)['files']]
assert len(reports) == 2
for report in reports:
    traits = {t['id']: t['crit'] for t in report.get('traits', [])}
    assert traits.get('micro-behaviors/data/format/credentials::discord-standard-token-regex-source') == 3
    assert not any(c >= 4 for c in traits.values()), (report['path'], traits)
print('Passed 2 passive token-pattern controls')
