#!/usr/bin/env python3
"""swift-base64-shell-loader needs every leg in one source neighborhood.

Run `python3 testdata/swift-base64-shell-loader/check.py <scratch-directory>`.
Fixtures are copied outside testdata so file-path testing suppressors cannot
mask the findings under test.
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
hostile = ('objectives/command-and-control/dropper/script-eval/embedded::'
           'swift-base64-shell-loader')
expected = {
    'split-capabilities-negative.zip': set(),
    'swift-dropper-positive.swift': {hostile},
    'swift-shell-only-negative.swift': set(),
}
for fixture in sorted(Path(__file__).parent.iterdir()):
    if fixture.suffix not in ('.swift', '.zip'):
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
        found |= {t['id'] for t in entry['traits'] if t['crit'] == 5}
    assert found == expected[fixture.name], (fixture.name, sorted(found))
    print(f'{fixture.name}: passed')
