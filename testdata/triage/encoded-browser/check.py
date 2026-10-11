#!/usr/bin/env python3
"""Run encoded-browser positive, renamed-source and benign near-miss controls."""
import json
import os
from pathlib import Path
import subprocess

repo = Path(__file__).resolve().parents[3]
cases = json.loads((Path(__file__).parent / 'cases.json').read_text())['fixtures']
proc = subprocess.run(
    [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(repo),
     '--format', 'json', *[str(repo / c['path']) for c in cases]],
    text=True, capture_output=True, check=True,
    env={**os.environ, 'CLEAVE_SKIP_CACHE': '1'}, timeout=300,
)
if proc.stderr.strip():
    raise AssertionError(proc.stderr)
reports = {}
remaining = proc.stdout
while remaining.strip():
    report, end = json.JSONDecoder().raw_decode(remaining.lstrip())
    remaining = remaining.lstrip()[end:]
    for file in report['files']:
        reports[str(Path(file['path']).resolve())] = file
for case in cases:
    file = reports[str((repo / case['path']).resolve())]
    traits = {t['id']: t for t in file.get('traits', [])}
    for trait in case['matched']:
        assert trait in traits, (case['path'], 'missing', trait)
    for trait in case['not_matched']:
        assert trait not in traits, (case['path'], 'unexpected', trait)
    if case['no_hostile']:
        hostile = [t for t in traits.values() if t['crit'] >= 5]
        assert not hostile, (case['path'], hostile)
print(f"Passed {len(cases)} encoded-browser controls")
