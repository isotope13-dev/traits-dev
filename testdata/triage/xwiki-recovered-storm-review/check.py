#!/usr/bin/env python3
"""Static-only checks; fixtures are parsed, never imported or executed."""
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
CASES = json.loads((HERE / 'cases.json').read_text())
with tempfile.TemporaryDirectory(prefix='.fallout-controls-', dir=ROOT) as name:
    targets = []
    for filename in CASES:
        target = Path(name) / filename
        shutil.copyfile(HERE / filename, target)
        targets.append(str(target))
    run = subprocess.run(['cleave', '--traits-dir', str(ROOT), '--format', 'jsonl',
                          'analyze', *targets], check=True, capture_output=True, text=True)
    reports = {
        Path(f['path']).name: {t['id']: t['crit'] for t in f.get('traits', [])}
        for line in run.stdout.splitlines() if line.strip()
        for f in json.loads(line).get('files', [])
        if f['path'] in targets
    }
    for filename, (required, forbidden) in CASES.items():
        actual = reports[filename]
        assert set(required) <= actual.keys(), (filename, 'missing', set(required) - actual.keys())
        assert not set(forbidden) & actual.keys(), (filename, 'unexpected', set(forbidden) & actual.keys())
        for trait in required:
            if trait.startswith(('metadata/', 'micro-behaviors/')):
                assert actual[trait] >= 3, (filename, 'capability below notable', trait)
print(f'{len(CASES)} static positive and near-miss cases passed')
