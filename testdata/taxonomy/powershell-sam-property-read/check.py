#!/usr/bin/env python3
"""Verify SAM access detection without treating comments as registry reads."""
import argparse
import json
import os
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--cleave', default='cleave')
parser.add_argument('--cases', type=Path, default=Path(__file__).with_name('cases.json'))
args = parser.parse_args()
repo = Path(__file__).resolve().parents[3]
cases = json.loads(args.cases.read_text())['fixtures']
result = subprocess.run(
    [args.cleave, '--traits-dir', str(repo), '--format', 'jsonl',
     *[case['path'] for case in cases]],
    cwd=repo, env=dict(os.environ, CLEAVE_VALIDATE='0'),
    text=True, capture_output=True, check=True,
)
files = {}
for line in result.stdout.splitlines():
    for file in json.loads(line).get('files', []):
        files[file['path']] = {trait['id'] for trait in file.get('traits', [])}
for case in cases:
    findings = files[case['path']]
    missing = set(case['matched']) - findings
    unexpected = set(case['not_matched']) & findings
    assert not missing and not unexpected, (case['case_id'], missing, unexpected)
print(f'{len(cases)} trait controls passed')
