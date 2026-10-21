#!/usr/bin/env python3
"""Check semantic controls against an already collected cleave JSON report."""
import json
from pathlib import Path
import sys

cases = json.loads(Path(__file__).with_name('cases.json').read_text())['fixtures']
reports = []
remaining = Path(sys.argv[1]).read_text().strip()
while remaining:
    report, end = json.JSONDecoder().raw_decode(remaining)
    reports.append(report)
    remaining = remaining[end:].lstrip()
files = [f for report in reports for f in report.get('raw', report)['files']]
failures = []
for case in cases:
    hits = [f for f in files if Path(f['path']).resolve() == Path(case['path']).resolve()]
    if len(hits) != 1:
        failures.append(f"{case['path']}: expected one analyzed file, got {len(hits)}")
        continue
    traits = {t['id'] for t in hits[0].get('traits', [])}
    for expected in case['matched']:
        if expected not in traits:
            failures.append(f"{case['path']}: missing {expected}")
    for unexpected in case['not_matched']:
        if unexpected in traits:
            failures.append(f"{case['path']}: unexpected {unexpected}")
    for trait in hits[0].get('traits', []):
        if trait.get('crit') in (4, 5, 'suspicious', 'hostile'):
            failures.append(f"{case['path']}: unexpected high severity {trait['id']}")
if failures:
    raise SystemExit('\n'.join(failures))
print(f'{len(cases)} semantic controls passed')
