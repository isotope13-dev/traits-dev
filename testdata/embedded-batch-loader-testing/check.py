#!/usr/bin/env python3
"""embedded-batch-self-reading-loader spares quoting unit tests.

Run `python3 testdata/embedded-batch-loader-testing/check.py
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
trait = ('micro-behaviors/data/format/script::'
         'embedded-batch-self-reading-loader')
expected = {
    'embedded-loader-positive.ts': {trait},
    'quoting-assertion-negative.test.ts': set(),
}
for fixture in sorted(Path(__file__).parent.glob('*.ts')):
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
