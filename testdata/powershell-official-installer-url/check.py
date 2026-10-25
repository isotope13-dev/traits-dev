#!/usr/bin/env python3
"""Official installer one-liners are not pipe-to-shell droppers.

Run `python3 testdata/powershell-official-installer-url/check.py
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
prefix = ('objectives/command-and-control/dropper/script-eval/'
          'response-pipeline::')
watched = {
    prefix + 'ps-iwr-pipeline-eval',
    prefix + 'ps-command-wrapper-useb-remote-eval',
    prefix + 'ps-network-eval-pipeline',
}
canonical = ('micro-behaviors/process/deploy/script-eval::'
             'powershell-web-response-piped-eval-text')
expected = {
    'install-doc-negative.md': set(),
    'untrusted-pipe-positive.ps1': set(),
}
for fixture in sorted(Path(__file__).parent.iterdir()):
    if fixture.name not in expected:
        continue
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
    capabilities = set()
    for entry in report['files']:
        capabilities |= {t['id'] for t in entry['traits'] if t['crit'] == 3}
        found |= {t['id'] for t in entry['traits']
                  if t['id'] in watched and t['crit'] == 4}
    assert found == expected[fixture.name], (fixture.name, sorted(found))
    if fixture.name == 'untrusted-pipe-positive.ps1':
        assert canonical in capabilities, (fixture.name, capabilities)
    print(f'{fixture.name}: passed')
