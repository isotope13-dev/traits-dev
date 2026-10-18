"""Run behavioral positives and near misses in one Cleave invocation."""
import json
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[3]
cases = json.loads(Path(__file__).with_name('cases.json').read_text())['fixtures']
result = subprocess.run(
    [sys.argv[1] if len(sys.argv) > 1 else 'cleave', '--format', 'json',
     *[case['path'] for case in cases]],
    cwd=root, text=True, capture_output=True, check=True,
)
reports = []
remaining = result.stdout.lstrip()
while remaining:
    report, end = json.JSONDecoder().raw_decode(remaining)
    reports.append(report)
    remaining = remaining[end:].lstrip()
files = {Path(f['path']).name: f for report in reports for f in report['files']}
errors = []
for case in cases:
    f = files[Path(case['path']).name]
    emitted = {trait['id'] for trait in f.get('traits', [])}
    for trait in case['required_emitted']:
        if trait not in emitted:
            errors.append(f"{case['path']}: missing {trait}")
    for trait in case['forbidden_emitted']:
        if trait in emitted:
            errors.append(f"{case['path']}: unexpected {trait}")
if errors:
    raise SystemExit('\n'.join(errors))
print(f'{len(cases)} behavioral controls passed')
