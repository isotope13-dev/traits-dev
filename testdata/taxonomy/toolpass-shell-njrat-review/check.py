#!/usr/bin/env python3
"""Regression controls for neutral capabilities and attack admission."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--cleave', default='cleave')
p.add_argument('--scratch-dir', required=True)
a = p.parse_args()
b = Path(__file__).parent
with tempfile.TemporaryDirectory(prefix='trait-review-', dir=a.scratch_dir) as tmp:
    for case in json.loads((b / 'cases.json').read_text())['fixtures']:
        target = Path(tmp) / case['file']
        shutil.copyfile(b / case['file'], target)
        proc = subprocess.run([a.cleave, '--no-update-check', '--traits-dir', str(ROOT),
                               '--disable', 'radare2,upx', '--format', 'json', str(target)],
                              text=True, capture_output=True,
                              env={**os.environ, 'CLEAVE_SKIP_CACHE': '1'})
        assert proc.returncode == 0, proc.stderr + proc.stdout
        report = json.loads(proc.stdout)
        findings = [t for f in report['files'] for t in f.get('traits', [])]
        ids = {t['id'] for t in findings}
        assert set(case.get('required', [])) <= ids, (case['file'], 'missing', set(case.get('required', [])) - ids, proc.stderr)
        assert not set(case.get('forbidden', [])) & ids, (case['file'], 'unexpected', set(case['forbidden']) & ids)
        if 'max_criticality' in case:
            assert all(t['crit'] <= case['max_criticality'] for t in findings), (case['file'], [t for t in findings if t['crit'] > case['max_criticality']])
        print('PASS', case['file'])
