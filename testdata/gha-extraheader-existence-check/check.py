#!/usr/bin/env python3
"""gha-checkout-extraheader-read spares exit-status existence checks.

Run `python3 testdata/gha-extraheader-existence-check/check.py
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
trait = ('objectives/supply-chain/trojanized/ci-pipeline::'
         'gha-checkout-extraheader-read')
expected = {
    'existence-check-negative.sh': set(),
    'token-exfil-positive.sh': {trait},
}
for fixture in sorted(Path(__file__).parent.glob('*.sh')):
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
    if expected[fixture.name]:
        assert expected[fixture.name] <= found, (fixture.name, sorted(found))
    else:
        assert found == set(), (fixture.name, sorted(found))
    print(f'{fixture.name}: passed')
