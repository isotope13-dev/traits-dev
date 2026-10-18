#!/usr/bin/env python3
"""Check controls on neutral paths, without test-directory suppressors."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[3]
cases = json.loads(Path(__file__).with_name('cases.json').read_text())
with tempfile.TemporaryDirectory(prefix='cleave-binding-') as tmp:
    for case in cases['fixtures']:
        source = repo / case['path']
        shutil.copyfile(source, Path(tmp) / source.name)
    run = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(repo),
         '--format', 'json', tmp], text=True, capture_output=True, check=True)
    # Directory scans may concatenate report objects without newlines.
    reports = []
    remaining = run.stdout.strip()
    decoder = json.JSONDecoder()
    while remaining:
        report, end = decoder.raw_decode(remaining)
        reports.append(report)
        remaining = remaining[end:].lstrip()
    files = {Path(f['path']).name: f
             for report in reports for f in report['files']}
    for case in cases['fixtures']:
        name = Path(case['path']).name
        matched = {t['id'] for t in files[name].get('traits', [])}
        missing = set(case['matched']) - matched
        unexpected = set(case['not_matched']) & matched
        assert not missing and not unexpected, (name, missing, unexpected)
        print(f'PASS {name}')
