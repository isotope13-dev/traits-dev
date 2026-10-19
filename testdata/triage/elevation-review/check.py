#!/usr/bin/env python3
"""Exercise UAC admission, provider separation, and neutral argument placement."""
import argparse
import json
import subprocess
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
cases = json.loads(Path(__file__).with_name('cases.json').read_text())['fixtures']
result = subprocess.run(
    [args.cleave, '--traits-dir', '.', '--format', 'jsonl',
     *[case['path'] for case in cases]],
    check=True, capture_output=True, text=True,
)
if result.stderr.strip():
    raise AssertionError(result.stderr)
reports = {}
text = result.stdout
while text.strip():
    report, end = json.JSONDecoder().raw_decode(text.lstrip())
    text = text.lstrip()[end:]
    reports.update({file['path']: file for file in report['files']})
for case in cases:
    report = reports[case['path']]
    ids = {trait['id'] for trait in report['traits']}
    assert set(case['matched']) <= ids, (case['path'], 'missing', set(case['matched']) - ids)
    assert not set(case['not_matched']) & ids, (case['path'], 'false positive', set(case['not_matched']) & ids)
    high = sum(trait['crit'] >= 4 for trait in report['traits'])
    assert high == case['high_count'], (case['path'], 'high criticality count', high)
print(f"Passed {len(cases)} focused controls")
