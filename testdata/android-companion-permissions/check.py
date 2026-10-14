#!/usr/bin/env python3
"""android-sensitive-access-permissions spares the OpenClaw companion app.

Run `python3 testdata/android-companion-permissions/check.py
<scratch-directory>`. Fixtures are copied outside testdata so file-path
testing suppressors cannot mask the findings under test.
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
trait = ('micro-behaviors/os/privilege/manifest::'
         'android-sensitive-access-permissions')
expected = {
    'companion-app-negative.zip': set(),
    'flashlight-spyware-positive.zip': {trait},
}
for fixture in sorted(Path(__file__).parent.glob('*.zip')):
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
        found |= {t['id'] for t in entry.get('traits', [])
                  if t['id'] == trait and t['crit'] == 4}
    assert found == expected[fixture.name], (fixture.name, sorted(found))
    print(f'{fixture.name}: passed')
