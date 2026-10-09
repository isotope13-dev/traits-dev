#!/usr/bin/env python3
"""Verify fixtures outside directories that suppress testing examples."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('--scratch-root', type=Path, required=True)
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
fixtures = Path(__file__).resolve().parent
root = fixtures.parents[2]
cases = json.loads((fixtures / 'cases.json').read_text())
with tempfile.TemporaryDirectory(prefix='conviction-controls-', dir=args.scratch_root) as stage:
    for name in cases:
        shutil.copyfile(fixtures / name, Path(stage) / name)
    result = subprocess.run(
        [args.cleave, '--traits-dir', str(root), '--format', 'json', stage],
        text=True, capture_output=True, check=True,
    )
    decoder = json.JSONDecoder()
    remaining = result.stdout
    reports = {}
    while remaining.strip():
        report, end = decoder.raw_decode(remaining.lstrip())
        remaining = remaining.lstrip()[end:]
        for item in report['files']:
            name = Path(item['path']).name
            if name in cases:
                reports[name] = item
    assert reports.keys() == cases.keys(), (reports.keys(), cases.keys())
    for name, expectations in cases.items():
        traits = {item['id']: item for item in reports[name].get('traits', [])}
        for trait, expected in expectations.items():
            assert (trait in traits) == expected, (name, trait, expected)
        if name not in {'cradle.ps1', 'encoded-code.py', 'overwrite.com'}:
            assert all(item['crit'] < 4 for item in traits.values()), (name, traits)
    print(f'{len(cases)} controls passed, including zero suspicious/hostile benign controls')
