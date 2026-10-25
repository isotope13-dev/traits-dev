"""Inspect fixtures statically; never import or execute them."""
import json
import os
from pathlib import Path
import subprocess

here = Path(__file__).resolve().parent
root = here.parents[1]
rule = 'micro-behaviors/fs/path-ops/join::python-query-stripped-basename-join'
result = subprocess.run([
    os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(root),
    '--format', 'json', str(here / 'fixtures'),
], capture_output=True, text=True, check=True)
assert not result.stderr.strip(), result.stderr
found = {}
remaining = result.stdout
while remaining.strip():
    report, end = json.JSONDecoder().raw_decode(remaining.lstrip())
    remaining = remaining.lstrip()[end:]
    for unit in report['files']:
        found[Path(unit['path']).name] = {
            t['id'] for t in unit.get('traits', [])
        }
for filename, expected in {
    'asset-path.py': True,
    'renamed-path.py': True,
    'near-misses.py': False,
}.items():
    assert (rule in found[filename]) == expected, (filename, found[filename])
    print('PASS', filename)
