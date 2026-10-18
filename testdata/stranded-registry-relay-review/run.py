"""Focused controls for neutral service/cipher facts and relay declarations."""
import json
import os
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[2]
cases = json.loads(Path(__file__).with_name('cases.json').read_text())
for case in cases['fixtures']:
    result = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(root),
         '--format', 'json', str(root / case['path'])],
        text=True, capture_output=True, check=True,
    )
    debug = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(root),
         'test-rules', str(root / case['path']), '--rules',
         ','.join(case['matched'] + case['not_matched'])],
        text=True, capture_output=True, check=True,
    )
    matched = {line.split()[1] for line in debug.stdout.splitlines()
               if line.startswith('MATCHED ')}
    report = json.loads(result.stdout)
    traits = {t['id']: t for f in report['files'] for t in f.get('traits', [])}
    for wanted in case['matched']:
        assert wanted in matched, (case['path'], 'missing', wanted)
    for unwanted in case['not_matched']:
        assert unwanted not in matched, (case['path'], 'unexpected', unwanted)
    if 'request-system' not in case['path']:
        assert not any(t['crit'] >= 4 for t in traits.values()), case['path']
    print(case['path'], 'PASS')
