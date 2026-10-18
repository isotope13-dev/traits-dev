"""Run the focused trait-placement and loop-equivalence fixtures."""
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
CASES = json.loads(Path(__file__).with_name('cases.json').read_text())['fixtures']
command = [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
           'analyze', '--format', 'json'] + [str(ROOT / c['path']) for c in CASES]
result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=True)
remaining = result.stdout
reports = []
decoder = json.JSONDecoder()
while remaining.strip():
    report, end = decoder.raw_decode(remaining.lstrip())
    reports.extend(report.get('files', [report]))
    remaining = remaining.lstrip()[end:]
by_name = {Path(r['path']).name: r for r in reports}
for case in CASES:
    report = by_name[Path(case['path']).name]
    ids = {t['id'] for t in report.get('traits', report.get('findings', []))}
    expected = set(case['matched'])
    forbidden = set(case['not_matched']) | set(case['forbidden_emitted'])
    assert expected <= ids, (case['case_id'], 'missing', expected - ids)
    assert not forbidden & ids, (case['case_id'], 'unexpected', forbidden & ids)
print(f'{len(CASES)} focused fixtures passed')
