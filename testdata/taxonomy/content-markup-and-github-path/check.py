#!/usr/bin/env python3
"""Exercise controls outside test-directory suppressors; never execute inputs."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

fixtures = Path(__file__).resolve().parent
repo = fixtures.parents[2]
parser = argparse.ArgumentParser()
parser.add_argument('--cleave', default=os.environ.get('CLEAVE', 'cleave'))
parser.add_argument('--scratch', required=True, type=Path)
args = parser.parse_args()
cases = json.loads((fixtures / 'cases.json').read_text())['fixtures']
with tempfile.TemporaryDirectory(prefix='markup-path-controls-', dir=args.scratch) as work:
    staged = Path(work) / 'inputs'
    shutil.copytree(fixtures, staged, ignore=shutil.ignore_patterns('cases.json', 'review.json', 'check.py'))
    result = subprocess.run([args.cleave, '--traits-dir', str(repo), '--format', 'json',
                             'analyze', str(staged)], capture_output=True, text=True)
    if result.returncode:
        print(result.stderr)
        print(result.stdout[:3000])
        raise SystemExit(result.returncode)
    decoder = json.JSONDecoder()
    text = result.stdout
    reports = {}
    while text.strip():
        text = text.lstrip()
        report, end = decoder.raw_decode(text)
        text = text[end:]
        for file in report['files']:
            relative = str(Path(file['path']).relative_to(staged))
            reports[relative] = {trait['id'] for trait in file.get('traits', [])}
    for case in cases:
        relative = str(Path(case['path']).relative_to(fixtures.relative_to(repo)))
        observed = reports[relative]
        missing = set(case['matched']) - observed
        unexpected = set(case['not_matched']) & observed
        assert not missing and not unexpected, (relative, missing, unexpected)
print(f'PASS: {len(cases)} controls; positive matches and near misses preserved')
