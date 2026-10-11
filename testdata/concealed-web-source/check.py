#!/usr/bin/env python3
"""Check meaningful positive and near-miss web-source fixtures."""
import json
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[2]
cases = json.loads((Path(__file__).with_name('cases.json')).read_text())['fixtures']
if len(sys.argv) == 2:
    output = Path(sys.argv[1]).read_text()
else:
    output = subprocess.check_output(
        ['cleave', '--traits-dir', str(root), '--disable', 'third-party',
         '--format', 'json', *[str(root / case['path']) for case in cases]],
        text=True,
    )
reports = []
decoder = json.JSONDecoder()
while output.strip():
    output = output.lstrip()
    report, end = decoder.raw_decode(output)
    reports.extend(report['files'])
    output = output[end:]
for case in cases:
    report = next(r for r in reports if r['path'].endswith(case['path']))
    traits = {t['id']: t for t in report['traits']}
    assert not set(case['matched']) - traits.keys(), case['path']
    assert not set(case['not_matched']) & traits.keys(), case['path']
    if case['path'].endswith('error-handler.html'):
        assert traits['micro-behaviors/data/control-flow/error-handling::onerror-after-return-true']['crit'] == 3
    if case['path'].endswith(('document-unescape.html', 'object-unescape.html')):
        assert not any(t.startswith('micro-behaviors/fs/write/') for t in traits)
print(f"PASS: {len(cases)} web-source controls")
