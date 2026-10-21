#!/usr/bin/env python3
"""Check retained attack coverage and API-query/browser-check near misses."""
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CASES = json.loads((HERE / 'cases.json').read_text())['fixtures']
result = subprocess.run(
    ['cleave', '--traits-dir', str(ROOT), '--format', 'json',
     *(case['path'] for case in CASES)],
    cwd=ROOT, capture_output=True, text=True, check=True,
)
remaining = result.stdout
reports = []
decoder = json.JSONDecoder()
while remaining.strip():
    remaining = remaining.lstrip()
    report, end = decoder.raw_decode(remaining)
    reports.append(report)
    remaining = remaining[end:]
findings = {
    file['path']: {trait['id'] for trait in file.get('traits', [])}
    for report in reports for file in report.get('files', [])
}
for case in CASES:
    seen = set().union(*(
        traits for path, traits in findings.items()
        if path == case['path'] or path.startswith(case['path'] + '!!')
    ))
    missing = set(case['matched']) - seen
    unexpected = set(case['not_matched']) & seen
    assert not missing and not unexpected, (case['path'], missing, unexpected)
    print('PASS', case['path'])
