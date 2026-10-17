"""Check positive and partial-evidence controls against the working traits."""
import argparse
import json
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
root = Path(__file__).parent
repo = root.parents[2]
cases = json.loads((root / 'cases.json').read_text())['fixtures']
result = subprocess.run([args.cleave, '--traits-dir', str(repo), '--format',
                         'json', *[case['path'] for case in cases]],
                        cwd=repo, text=True, capture_output=True, check=True)
decoder = json.JSONDecoder()
reports = []
remaining = result.stdout.strip()
while remaining:
    report, end = decoder.raw_decode(remaining)
    reports.append(report)
    remaining = remaining[end:].lstrip()
by_path = {item['path']: {trait['id'] for trait in item.get('traits', [])}
           for report in reports for item in report['files']}
for case in cases:
    emitted = by_path[case['path']]
    missing = set(case['required_emitted']) - emitted
    unexpected = set(case['forbidden_emitted']) & emitted
    assert not missing and not unexpected, (case['case_id'], missing, unexpected)
    print('PASS', case['case_id'])
