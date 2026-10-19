"""Check positive and near-miss cases against the current trait tree."""
import json
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parent
repo = root.parents[2]
cases = json.loads((root / 'cases.json').read_text())['fixtures']
result = subprocess.run([sys.argv[1] if len(sys.argv) > 1 else 'cleave',
                         '--traits-dir', str(repo), '--format', 'json',
                         *[case['path'] for case in cases]],
                        cwd=repo, text=True, capture_output=True)
if result.returncode:
    sys.exit(result.stderr or result.stdout)
reports = []
pending = result.stdout.lstrip()
decoder = json.JSONDecoder()
while pending:
    report, end = decoder.raw_decode(pending)
    reports.append(report)
    pending = pending[end:].lstrip()
by_name = {Path(item['path']).name: item for report in reports for item in report['files']}
errors = []
for case in cases:
    observed = {trait['id'] for trait in by_name[Path(case['path']).name]['traits']}
    errors.extend(f"{case['path']}: missing {item}" for item in case['matched'] if item not in observed)
    errors.extend(f"{case['path']}: unexpected {item}" for item in case['not_matched'] if item in observed)
if errors:
    sys.exit('\n'.join(errors))
print(f"PASS: {len(cases)} positive and near-miss fixtures")
