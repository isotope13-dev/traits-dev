#!/usr/bin/env python3
"""Check focused rules, preserving other independent findings on near misses."""
import json
import sys
from pathlib import Path

base = Path(__file__).resolve().parent
reports = Path(sys.argv[1]).read_text()
decoder = json.JSONDecoder()
observed = {}
while reports.strip():
    report, end = decoder.raw_decode(reports.lstrip())
    reports = reports.lstrip()[end:]
    for item in report.get('files', []):
        if '!!' not in item['path']:
            observed[Path(item['path']).name] = {t['id'] for t in item.get('traits', [])}
for name, expectation in json.loads((base / 'cases.json').read_text()).items():
    assert name in observed, f'missing report: {name}'
    actual = observed[name]
    assert set(expectation.get('require', [])) <= actual, (name, 'missing', set(expectation.get('require', [])) - actual)
    assert not set(expectation.get('forbid', [])) & actual, (name, 'unexpected', set(expectation.get('forbid', [])) & actual)
print(f'Passed {len(json.loads((base / "cases.json").read_text()))} focused file controls')
