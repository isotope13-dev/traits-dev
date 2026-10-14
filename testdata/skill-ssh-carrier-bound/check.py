#!/usr/bin/env python3
"""packaged-agent-skill-ssh-key-tunnel still convicts small skill packages.

Run `python3 testdata/skill-ssh-carrier-bound/check.py <scratch-directory>`.
The fixture is copied outside testdata so file-path testing suppressors
cannot mask the findings under test. There is no committable negative for
the 32MB carrier bound (it only bites on monorepo-scale archives); the
OpenClaw source tree is the real-world negative, documented in the README.
"""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

scratch = Path(sys.argv[1])
scratch.mkdir(parents=True, exist_ok=True)
root = Path(__file__).resolve().parents[2]
trait = ('objectives/lateral-movement/ssh/deploy-backdoor::'
         'packaged-agent-skill-ssh-key-tunnel')
fixture = Path(__file__).parent / 'evil-skill-positive.zip'
target = scratch / fixture.name
shutil.copyfile(fixture, target)
result = subprocess.run(
    [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(root),
     '--format', 'json', str(target)],
    env=dict(os.environ, CLEAVE_VALIDATE='0'), text=True,
    capture_output=True, check=True,
)
report = json.loads(result.stdout)
found = set()
for entry in report['files']:
    found |= {t['id'] for t in entry['traits']
              if t['id'] == trait and t['crit'] == 4}
assert found == {trait}, (fixture.name, sorted(found))
print(f'{fixture.name}: passed')
