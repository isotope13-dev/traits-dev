#!/usr/bin/env python3
"""Check source/capability placement and retained WhatsApp theft coverage."""
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
CASES = Path(__file__).with_name('cases.json')

def main():
    cases = json.loads(CASES.read_text())
    for case in cases['fixtures']:
        result = subprocess.run(
            [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
             '--format', 'json', str(ROOT / case['path'])],
            check=True, capture_output=True, text=True)
        data = json.loads(result.stdout)
        findings = {trait['id'] for file in data['files']
                    for trait in file.get('traits', [])}
        missing = set(case.get('matched', [])) - findings
        extra = set(case.get('not_matched', [])) & findings
        assert not missing and not extra, (case['case_id'], missing, extra)
        if case['case_id'] == 'registry-open-wa-init-patch':
            assert not any(t['crit'] >= 5 for f in data['files']
                           for t in f.get('traits', [])), 'unsupported hostile finding'
        print(case['case_id'] + ': PASS')

if __name__ == '__main__':
    main()
