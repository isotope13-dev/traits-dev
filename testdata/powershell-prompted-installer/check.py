#!/usr/bin/env python3
"""Operator-prompted installers are not poll-eval agents.

Run `python3 testdata/powershell-prompted-installer/check.py
<scratch-directory>`. Fixtures are copied outside testdata so file-path
testing suppressors cannot mask the findings under test.

`agent-loop-positive.ps1` is a canonical tight agent loop (unbounded loop
retrieves a task body, evaluates it, sleeps): it must report the
http-poll-eval-agent-loop hostile.

`prompted-installer-negative.ps1` is an interactive installer (the unbounded
loop prompts the operator via Read-Host, the sleep is retry backoff, the
fetched script executes once): the hostile must stay silent while the
read-host-call notable marks the operator read.
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
watched = {
    ('objectives/command-and-control/remote-command/tasking::'
     'http-poll-eval-agent-loop', 5),
    ('micro-behaviors/os/console/io::read-host-call', 3),
}
expected = {
    'agent-loop-positive.ps1': {
        ('objectives/command-and-control/remote-command/tasking::'
         'http-poll-eval-agent-loop', 5),
    },
    'prompted-installer-negative.ps1': {
        ('micro-behaviors/os/console/io::read-host-call', 3),
    },
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
    for entry in report['files']:
        found |= {(t['id'], t['crit']) for t in entry['traits']
                  if (t['id'], t['crit']) in watched}
    assert found == expected[fixture.name], (fixture.name, sorted(found))
    print(f'{fixture.name}: passed')
