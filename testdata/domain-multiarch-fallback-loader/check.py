#!/usr/bin/env python3
"""Domain-held multi-arch fallback loaders are bot droppers.

Run `python3 testdata/domain-multiarch-fallback-loader/check.py
<scratch-directory>`. Fixtures are copied outside testdata so file-path
testing suppressors cannot mask the findings under test.

`loader-positive.sh` is a sanitized Mirai-style loader (documentation
domain, so inert): variable-held domain host, multi-client fallback down
to a raw /dev/tcp socket, per-architecture selection, chmod 777, detached
local execution. It must report both hostiles,
domain-multiarch-protocol-dropper and multiarch-protocol-literal-exec.

`installer-negative.sh` is an ordinary per-architecture release installer
(single HTTP client, chmod +x, foreground relative-path launch, no raw
socket): it must report neither hostile.

The positive must also surface the relocated neutral
dev-tcp-variable-port-80 notable, and must never reference the removed
well-known mirror-tcp-probe id.
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
IOT = ('objectives/command-and-control/botnet/iot::'
       'domain-multiarch-protocol-dropper')
SHELL = ('objectives/command-and-control/dropper/file-exec/command/shell::'
         'multiarch-protocol-literal-exec')
TCP = 'micro-behaviors/communications/socket/tcp::dev-tcp-variable-port-80'
OLD = ('well-known/app/storage/community-scripts-proxmoxve::'
       'mirror-tcp-probe')
watched = {(IOT, 5), (SHELL, 5), (TCP, 3)}
expected = {
    'loader-positive.sh': {(IOT, 5), (SHELL, 5), (TCP, 3)},
    'installer-negative.sh': set(),
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
    all_ids = set()
    for entry in report['files']:
        for t in entry['traits']:
            all_ids.add(t['id'])
            if (t['id'], t['crit']) in watched:
                found.add((t['id'], t['crit']))
    assert OLD not in all_ids, (fixture.name, 'removed id still fires')
    assert found == expected[fixture.name], (fixture.name, sorted(found))
    print(f'{fixture.name}: passed')
