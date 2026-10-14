#!/usr/bin/env python3
"""gha-secret-diagnostic-upload must ignore nested helper actions.

Run `python3 testdata/gha-diagnostic-upload-pooling/check.py
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
hostile = ('objectives/supply-chain/hidden-payload/ci::'
           'gha-secret-diagnostic-upload')
expected = {
    'nested-helper-negative.zip': set(),
    'published-action-positive.zip': {hostile},
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
        found |= {t['id'] for t in entry['traits'] if t['crit'] == 5}
    assert found == expected[fixture.name], (fixture.name, sorted(found))
    print(f'{fixture.name}: passed')
