#!/usr/bin/env python3
"""Scan inert source fixtures and check attack/capability boundaries."""
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
cases = json.loads((HERE / 'cases.json').read_text())
result = subprocess.run(
    ['cleave', '--traits-dir', str(ROOT), '--format', 'json',
     *[str(HERE / case['path']) for case in cases]],
    check=True, text=True, capture_output=True,
)
assert not result.stderr.strip(), result.stderr
files = {}
decoder = json.JSONDecoder()
remaining = result.stdout.strip()
while remaining:
    report, end = decoder.raw_decode(remaining)
    files.update({Path(f['path']).name: f for f in report['files']})
    remaining = remaining[end:].lstrip()
for case in cases:
    traits = {t['id']: t for t in files[case['path']]['traits']}
    for label, severity in [('hostile', 5), ('suspicious', 4)]:
        if label in case:
            actual = sum(t['crit'] == severity for t in traits.values())
            assert actual == case[label], (case['path'], label, actual)
    for trait, severity in case.get('required', {}).items():
        assert traits.get(trait, {}).get('crit') == severity, (case['path'], trait)
    for trait in case.get('absent', []):
        assert trait not in traits, (case['path'], trait)
print(f'{len(cases)} source capability and exploit boundary cases passed')
