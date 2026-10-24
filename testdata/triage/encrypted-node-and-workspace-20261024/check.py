#!/usr/bin/env python3
"""Exercise staging data bindings, shared-rule positives and nearby controls."""
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
CLEAVE = os.environ.get('CLEAVE', 'cleave')
cases = json.loads((HERE / 'cases.json').read_text())['fixtures']
result = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), '--format', 'json',
                         *[str(ROOT / c['path']) for c in cases]],
                        text=True, capture_output=True, check=True)
remaining = result.stdout.lstrip()
reports = []
decoder = json.JSONDecoder()
while remaining:
    report, end = decoder.raw_decode(remaining)
    reports.extend(report['files'])
    remaining = remaining[end:].lstrip()
found = {Path(f['path']).name: {t['id'] for t in f.get('traits', [])}
         for f in reports}
for case in cases:
    ids = found[Path(case['path']).name]
    missing = set(case['matched']) - ids
    if missing:
        debug = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), 'test-rules', str(ROOT / case['path']), '--rules', ','.join(missing)], text=True, capture_output=True, check=True)
        ids |= {line.split()[1] for line in debug.stdout.splitlines() if line.startswith('MATCHED ')}
    assert set(case['matched']) <= ids, (case['path'], 'missing', set(case['matched']) - ids)
    assert not set(case['not_matched']) & ids, (case['path'], 'unexpected', set(case['not_matched']) & ids)
# Low-tier omission facts can be stripped from reports; inspect rule truth too.
rule = 'metadata/permission/telemetry::gecko-data-collection-omitted'
for name, wanted in [('gecko-omitted.json', True), ('gecko-present.json', False),
                     ('workspace.json', False)]:
    r = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), 'test-rules',
                        str(HERE / name), '--rules', rule],
                       text=True, capture_output=True, check=True)
    matched = {line.split()[1] for line in r.stdout.splitlines() if line.startswith('MATCHED ')}
    assert (rule in matched) == wanted, (name, r.stdout)
print(f'{len(cases)} report controls and 3 Gecko rule controls passed')
