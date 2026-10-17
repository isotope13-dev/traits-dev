#!/usr/bin/env python3
"""Disguised-persistence WX-entry alternative coverage.

Run `python3 testdata/taxonomy/disguised-persistence-wx-entry/check.py
<scratch-directory>`. The subject is the case sample (copied to scratch
so file-path testing suppressors cannot mask the findings under test);
override with SAMPLE=<path>.

The infector parks its entry point in a random writable-and-executable
section instead of .reloc, while keeping the disguised svchost autorun
command with Run-key writes and service creation. This pins both
disguised-persistence hostile composites firing through the WX-entry
alternative, and pins the reloc-entry atom absent to lock the variant
distinction.
"""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

SAMPLE = os.environ.get(
    'SAMPLE',
    '/usr/local/var/cyclotron/tmp.noindex/cyclotron-bb4ff6df/samples/'
    '09b76610cc6b/jaffacakes118_HEUR.Trojan.Win32.Generic.'
    '3a8991a5774aac4f849a0',
)

matched = {
    'objectives/persistence/login/registry/run-key::'
    'disguised-system-subdirectory-run-key',
    'objectives/persistence/system/service/install::'
    'disguised-system-subdirectory-service',
}
not_matched = {
    'metadata/binary/section/header::pe-entry-in-reloc-section',
}

scratch = Path(sys.argv[1]) / 'case'
scratch.mkdir(parents=True, exist_ok=True)
root = Path(__file__).resolve().parents[3]
target = scratch / Path(SAMPLE).name
shutil.copyfile(SAMPLE, target)
result = subprocess.run(
    [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(root),
     '--format', 'json', str(target)],
    env=dict(os.environ, CLEAVE_VALIDATE='0'), text=True,
    capture_output=True, check=True,
)
report = json.loads(result.stdout)
found = {t['id'] for f in report['files'] for t in f['traits']
         if t['crit'] >= 4}
found_all = {t['id'] for f in report['files'] for t in f['traits']}
missing = matched - found
leaked = not_matched & found_all
if missing or leaked:
    print(f'FAILED missing={sorted(missing)} leaked={sorted(leaked)}')
    sys.exit(1)
print('disguised-persistence-wx-entry: passed')
