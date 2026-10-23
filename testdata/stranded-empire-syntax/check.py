#!/usr/bin/env python3
"""Check that neutral syntax remains visible without losing attack composites."""
import argparse
import json
import os
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
repo = Path(__file__).resolve().parents[2]
env = os.environ.copy()
env.pop('CLEAVE_VALIDATE', None)
cases = json.loads(Path(__file__).with_name('cases.json').read_text())
for case in cases['fixtures']:
    result = subprocess.run(
        [args.cleave, '--traits-dir', str(repo), '--format', 'json', case['path']],
        cwd=repo, env=env, capture_output=True, text=True, check=True,
    )
    report = json.loads(result.stdout)
    emitted = {t['id']: t['crit'] for f in report['files'] for t in f.get('traits', [])}
    for trait, severity in case['required'].items():
        assert emitted.get(trait) == severity, (case['path'], trait, emitted.get(trait))
    for trait in case['forbidden']:
        assert trait not in emitted, (case['path'], trait)
    print('PASS', case['path'])
