#!/usr/bin/env python3
"""RFC 2606 placeholder hosts are not staged dylib payloads.

Run `python3 testdata/remote-dylib-placeholder/check.py
<scratch-directory>`. Fixtures are copied outside testdata so file-path
testing suppressors cannot mask the findings under test.

`fixture-placeholder-negative.py` mirrors the risset package-manager test
that referenced https://example.com/old.dylib: documentation-domain URLs
must not report source-remote-dylib-url.

`fixture-remote-positive.py` stages a dylib from a real remote host: it
must still report the suspicious trait.
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
DYLIB = ('objectives/evasion/hijack-execution-flow/dylib-hijacking::'
         'source-remote-dylib-url')
watched = {(DYLIB, 4)}
expected = {
    'fixture-placeholder-negative.py': set(),
    'fixture-remote-positive.py': {(DYLIB, 4)},
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
