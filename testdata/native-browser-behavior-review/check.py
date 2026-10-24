#!/usr/bin/env python3
"""Check changed exploit and driver contracts without executing fixtures."""
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
cases = json.loads((HERE / 'cases.json').read_text())
paths = [HERE / case['path'] for case in cases]
paths += [HERE / 'ccprotect-security-process.cpp',
          ROOT / 'testdata/registry-source-second-review/other-device.c',
          ROOT / 'testdata/registry-source-second-review/ioctl-value.c']
env = dict(os.environ, CLEAVE_VALIDATE='0')
run = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
                      '--format', 'json', *map(str, paths)],
                     env=env, capture_output=True, text=True, check=True)
decoder = json.JSONDecoder()
remaining = run.stdout.strip()
reports = {}
while remaining:
    report, end = decoder.raw_decode(remaining)
    reports.update({str(Path(f['path']).resolve()): f for f in report['files']})
    remaining = remaining[end:].lstrip()
for case in cases:
    traits = {t['id'] for t in reports[str(HERE / case['path'])].get('traits', [])}
    assert set(case['required']) <= traits, (case['path'], 'missing', traits)
    assert not set(case['forbidden']) & traits, (case['path'], 'unexpected', traits)
    print('PASS', case['path'])
killer = 'objectives/impact/degrade/edr/teardown::edr-killer-behavior'
traits = {t['id'] for t in reports[str(HERE / 'ccprotect-security-process.cpp')]['traits']}
assert killer in traits
for path in paths[-2:]:
    assert not any(t['crit'] >= 4 for t in reports[str(path)].get('traits', [])), path
print('PASS retained CcProtect attack and two existing benign near misses')
