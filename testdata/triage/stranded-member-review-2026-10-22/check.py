#!/usr/bin/env python3
"""Check wallet-ID placement, benign catalogs, and retained collector coverage."""
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
PREFIX = 'micro-behaviors/browser-extension/lifecycle::'
CASES = {
    'wallet-id-catalog.js': (23, False),
    'wallet-id-near-miss.js': (0, False),
    'connectkit-catalog.js': (5, False),
    'collector.py': (5, True),
}
for filename, (count, attack) in CASES.items():
    result = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT), '--json', str(HERE / filename)],
        check=True, capture_output=True, text=True,
    )
    report = json.loads(result.stdout)
    traits = report['files'][0]['traits']
    selected = [t for t in traits if t['id'].startswith(PREFIX)]
    assert len(selected) == count, (filename, len(selected), count)
    assert all(t['crit'] == 3 for t in selected), filename
    assert not any(t['id'].startswith('well-known/app/browser-extension/') and
                   ('extension-id' in t['id'] or 'wallet-extension' in t['id']) for t in traits), filename
    if attack:
        assert any(t['crit'] >= 4 and t['id'].startswith('objectives/') for t in traits), filename
    else:
        assert not any(t['crit'] >= 4 for t in traits), filename
    print(filename, 'passed')
