#!/usr/bin/env python3
"""Check allocation, protection-argument and kernel-exploit boundaries."""
import json
import os
from pathlib import Path
import subprocess

repo = Path(__file__).resolve().parents[3]
cases = json.loads(Path(__file__).with_name('cases.json').read_text())['fixtures']
result = subprocess.run(
    [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(repo), '--json',
     *[case['path'] for case in cases]],
    cwd=repo, check=True, text=True, capture_output=True,
)
reports = {
    report['path']: report
    for line in result.stdout.splitlines()
    for report in json.loads(line)['files']
}
for case in cases:
    traits = {trait['id']: trait['crit'] for trait in reports[case['path']].get('traits', [])}
    missing = set(case['matched']) - traits.keys()
    unexpected = set(case['not_matched']) & traits.keys()
    assert not missing and not unexpected, (case['path'], missing, unexpected)
    if not case['path'].endswith('renamed-bitmap-token-copy.ps1'):
        assert 5 not in traits.values(), (case['path'], 'unexpected hostile finding')
print(f"PASS: {len(cases)} memory and exploit boundary controls")
