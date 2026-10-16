#!/usr/bin/env python3
"""WSH environment-staged hidden-Run loader coverage.

Run `python3 testdata/taxonomy/wsh-env-staged-hidden-run/check.py
<scratch-directory>`. Fixtures are copied outside testdata so file-path
testing suppressors cannot mask the findings under test.

The WMI Create path has a Run fallback: the same environment-staged
command runs via WScript.Shell.Run with a hidden window. The positive
fixture stages two chunks through the User environment object, strips
non-ASCII markers, and hidden-runs the staged command; the benign admin
fixture runs a visible program with no staging or obfuscation.
"""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

LOADER = ('objectives/execution/interpreter/script/dropper::'
          'wsh-environment-staged-hidden-run-loader')
WMI_LOADER = ('objectives/execution/wmi::'
              'wsh-environment-staged-hidden-wmi-loader')

expected = {
    'env-staged-hidden-run.js': {
        'matched': {LOADER},
        'not_matched': {WMI_LOADER},
    },
    'benign-visible-run.js': {
        'matched': set(),
        'not_matched': {LOADER, WMI_LOADER},
    },
}

scratch = Path(sys.argv[1]) / 'case'
scratch.mkdir(parents=True, exist_ok=True)
root = Path(__file__).resolve().parents[3]
failed = False
for fixture, wants in sorted(expected.items()):
    target = scratch / fixture
    shutil.copyfile(Path(__file__).parent / fixture, target)
    result = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(root),
         '--format', 'json', str(target)],
        env=dict(os.environ, CLEAVE_VALIDATE='0'), text=True,
        capture_output=True, check=True,
    )
    report = json.loads(result.stdout)
    found = {t['id'] for f in report['files'] for t in f['traits']
             if t['crit'] >= 4}
    missing = wants['matched'] - found
    leaked = wants['not_matched'] & found
    if missing or leaked:
        failed = True
        print(f'{fixture}: FAILED missing={sorted(missing)} '
              f'leaked={sorted(leaked)}')
    else:
        print(f'{fixture}: passed')
sys.exit(1 if failed else 0)
