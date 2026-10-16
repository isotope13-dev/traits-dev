#!/usr/bin/env python3
"""Short-name batch slicing and hidden environment-staged execution.

Run `python3 testdata/taxonomy/batch-short-slice-stager/check.py
<scratch-directory>`. Fixtures are copied outside testdata so file-path
testing suppressors cannot mask the findings under test.

Covers the short-var slicing atom (4-5 character obfuscator names the
{6,} atom misses) staying disjoint from it, and the hidden
PowerShell environment-staged ScriptBlock composite, while a benign
admin script with a few slices and a visible PowerShell call stays
clean of both plus the fragment-built loader.
"""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

SHORT_SLICING = ('objectives/anti-static/obfuscation/string/fragmentation::'
                 'batch-short-var-substring-slicing')
LONG_SLICING = ('objectives/anti-static/obfuscation/string/fragmentation::'
                'batch-delayed-substring-slicing')
LOADER = ('objectives/anti-static/obfuscation/eval/powershell-loader::'
          'batch-fragment-built-powershell-scriptblock-loader')
HIDDEN_STAGED = ('objectives/evasion/process/hidden/execution::'
                 'batch-hidden-powershell-env-staged-scriptblock')

expected = {
    'short-slice-hidden-stager.bat': {
        'matched': {SHORT_SLICING, HIDDEN_STAGED},
        'not_matched': {LONG_SLICING},
    },
    'benign-slice-admin.bat': {
        'matched': set(),
        'not_matched': {SHORT_SLICING, LONG_SLICING, LOADER, HIDDEN_STAGED},
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
