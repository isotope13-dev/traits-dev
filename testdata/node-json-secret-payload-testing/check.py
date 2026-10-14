#!/usr/bin/env python3
"""node-json-secret-file-payload spares unit-test policy fixtures.

Run `python3 testdata/node-json-secret-payload-testing/check.py
<scratch-directory>`. Fixtures are copied outside testdata so file-path
testing suppressors cannot mask the findings under test.
"""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

scratch = Path(sys.argv[1]) / 'case'
scratch.mkdir(parents=True, exist_ok=True)
root = Path(__file__).resolve().parents[2]
trait = ('objectives/exfiltration/dns/encoded::'
         'node-json-secret-file-payload')
expected = {
    'exfil-shape-positive.js': {trait},
    'policy-shape-negative.test.ts': set(),
}
for fixture in sorted(Path(__file__).parent.iterdir()):
    if fixture.suffix not in ('.js', '.ts'):
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
    traits = report['files'][0]['traits']
    found = {t['id'] for t in traits if t['crit'] == 4}
    assert found == expected[fixture.name], (fixture.name, sorted(found))
    print(f'{fixture.name}: passed')
