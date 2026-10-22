"""Static rule controls; never execute the AppleScript or exploit payloads."""
import json
import os
from pathlib import Path
import subprocess

fixtures = Path(__file__).resolve().parent
root = fixtures.parents[2]
cases = json.loads((fixtures / 'cases.json').read_text())['fixtures']
result = subprocess.run(
    [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(root),
     '--format', 'jsonl', 'analyze', *[str(root / c['path']) for c in cases]],
    capture_output=True, text=True, check=False,
)
if result.returncode:
    raise RuntimeError(result.stderr)
reports = {}
for line in result.stdout.splitlines():
    for report in json.loads(line).get('files', []):
        reports[Path(report['path']).resolve()] = {
            t['id'] for t in report.get('traits', [])
        }
for case in cases:
    actual = reports[(root / case['path']).resolve()]
    missing = set(case['matched']) - actual
    unexpected = set(case['not_matched']) & actual
    assert not missing and not unexpected, (case['path'], missing, unexpected)
print(f'Passed {len(cases)} secret-staging and boundary cases')
