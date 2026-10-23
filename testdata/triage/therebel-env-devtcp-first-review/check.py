"""Static regression checks; never execute the sample source."""
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
cases = json.loads((HERE / 'cases.json').read_text())
result = subprocess.run(
    [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT), '--json',
     *[str(HERE / case['file']) for case in cases]],
    check=True, capture_output=True, text=True,
    env={**os.environ, 'CLEAVE_VALIDATE': '0'},
)
assert not result.stderr.strip(), result.stderr
reports = {}
for line in result.stdout.splitlines():
    for report in json.loads(line)['files']:
        reports[Path(report['path']).name] = {
            trait['id']: trait['crit'] for trait in report.get('traits', [])
        }
for case in cases:
    actual = reports[case['file']]
    for trait, expected in case['criticality'].items():
        assert actual.get(trait) == expected, (case['file'], trait, expected, actual.get(trait))
    for trait in case['absent']:
        assert trait not in actual, (case['file'], 'unexpected', trait)
    print('PASS', case['file'])
