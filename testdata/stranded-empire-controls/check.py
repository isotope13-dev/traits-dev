"""Check that neutral process names, policy co-occurrence and hive reports stay benign."""
import json
import os
import re
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parent
repo = root.parent.parent
context = dict(os.environ, CLEAVE_TRAITS_DIR=str(repo), CLEAVE_VALIDATE='0', SCAN_FETCH='none')
cases = json.loads((root / 'cases.json').read_text())
result = subprocess.run(
    ['atomscan', '--no-update', '--follow=none', '--mode', 'slow', '-f', 'json',
     *[str(root / case['file']) for case in cases]],
    env=context, capture_output=True, text=True,
)
reports = [json.loads(line) for line in result.stdout.splitlines() if line.strip()]
by_path = {Path(report['raw']['files'][0]['path']).resolve(): report for report in reports}
for case in cases:
    report = by_path[root / case['file']]
    traits = {t['id']: t for f in report['raw']['files'] for t in f.get('traits', [])}
    # OR-only grouping rules can be used by consumers without being rendered.
    # Inspect rule truth separately from the scan's analyst-facing findings.
    trace = subprocess.run(
        ['cleave', 'test-rules', '--rules',
         ','.join(case['present'] + case['absent']), str(root / case['file'])],
        env=context, capture_output=True, text=True, check=True,
    )
    matched = set(re.findall(r'^MATCHED (\S+)', trace.stdout, re.M))
    missing = set(case['present']) - matched
    unwanted = set(case['absent']) & matched
    hostile = [t['id'] for t in traits.values() if t['crit'] == 5]
    suspicious = [t['id'] for t in traits.values() if t['crit'] == 4]
    assert not missing and not unwanted, (case['file'], missing, unwanted)
    assert not hostile and len(suspicious) <= 1, (case['file'], hostile, suspicious)
    print('PASS', case['file'])
