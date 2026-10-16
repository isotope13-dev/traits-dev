#!/usr/bin/env python3
"""Svchost service-dropper variant and hook-chain keylogger coverage.

Run `python3 testdata/taxonomy/babar-service-hook-spy/check.py
<scratch-directory>`. The subject is the case sample (copied to scratch
so file-path testing suppressors cannot mask the findings under test);
override with SAMPLE=<path>.

The 360-masquerading installer skips the canonical Find/Load/Lock/Sizeof
chain yet still drops its embedded payload PE with timestomped writes
and registers it as a ServiceDll under svchost netsvcs (outer layer),
while the staged child installs a SetWindowsHookEx chain with registry
persistence, process control, and window-title capture. This pins both
new hostile composites on their layers, and pins the canonical
netsvcs-resource-service-dll-dropper absent to lock the variant
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
    '3a0d2e120764/jaffacakes118_HEUR.Trojan.Win32.Generic.'
    '1e91b4d137055d4eb64d328d47c7f6bc',
)

matched = {
    'objectives/persistence/system/service/loader::'
    'netsvcs-embedded-pe-service-file-dropper',
    'objectives/collection/keylog/hook::'
    'windows-hook-chain-persistence-keylogger',
}
not_matched = {
    'objectives/persistence/system/service/loader::'
    'netsvcs-resource-service-dll-dropper',
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
print('babar-service-hook-spy: passed')
