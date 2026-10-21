#!/usr/bin/env python3
"""Check parser/data near misses and retain separately evidenced API calls."""
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
CASES = json.loads(Path(__file__).with_name('cases.json').read_text())['fixtures']
ENGINE = os.environ.get('CLEAVE', 'cleave')
result = subprocess.run([ENGINE, '--traits-dir', str(ROOT), '--format', 'json',
                         *[str(ROOT / c['path']) for c in CASES]],
                        check=True, text=True, capture_output=True)
remaining, reports = result.stdout.strip(), {}
decoder = json.JSONDecoder()
while remaining:
    report, end = decoder.raw_decode(remaining)
    for file in report['files']:
        reports[Path(file['path']).name] = {t['id'] for t in file.get('traits', [])}
    remaining = remaining[end:].lstrip()
for case in CASES:
    ids = reports[Path(case['path']).name]
    missing, unexpected = set(case['matched']) - ids, set(case['not_matched']) & ids
    assert not missing and not unexpected, (case['path'], missing, unexpected)
    # Baseline jQuery observations may be stripped from emitted reports.
    for key, expected in [('trace_matched', 'MATCHED '), ('trace_not_matched', 'NOT MATCHED ')]:
        for trait in case.get(key, []):
            trace = subprocess.run([ENGINE, '--traits-dir', str(ROOT), 'test-rules',
                                    str(ROOT / case['path']), '--rules', trait],
                                   check=True, text=True, capture_output=True)
            assert any(line.startswith(expected + trait + ' ') for line in trace.stdout.splitlines()), trace.stdout
    print('PASS', Path(case['path']).name)
