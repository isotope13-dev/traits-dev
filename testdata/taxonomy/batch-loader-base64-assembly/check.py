#!/usr/bin/env python3
"""Fragment-built loader base64-assembly alternative coverage.

Run `python3 testdata/taxonomy/batch-loader-base64-assembly/check.py
<scratch-directory>`. The subject is the case sample (copied to scratch
so file-path testing suppressors cannot mask the findings under test);
override with SAMPLE=<path>.

The PRE-ALERT loader assembles its staged PowerShell from plain `set`
concatenation and base64 chunks with no substring slicing at all, so
both slicing atoms must stay absent while the fragment-built loader
composite still fires through the base64-payload alternative, next to
the hidden environment-staged execution composite.
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
    'ed048feaad26/PRE-ALERT_6055092726.rar',
)

matched = {
    'objectives/anti-static/obfuscation/eval/powershell-loader::'
    'batch-fragment-built-powershell-scriptblock-loader',
    'objectives/evasion/process/hidden/execution::'
    'batch-hidden-powershell-env-staged-scriptblock',
}
not_matched = {
    'objectives/anti-static/obfuscation/string/fragmentation::'
    'batch-delayed-substring-slicing',
    'objectives/anti-static/obfuscation/string/fragmentation::'
    'batch-short-var-substring-slicing',
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
missing = matched - found
leaked = not_matched & found
if missing or leaked:
    print(f'FAILED missing={sorted(missing)} leaked={sorted(leaked)}')
    sys.exit(1)
print('batch-loader-base64-assembly: passed')
