#!/usr/bin/env python3
"""Endpoint collection tokens must ignore relative module requires.

Run `python3 testdata/url-endpoint-relative-require/check.py <scratch-directory>`.
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
prefix = 'micro-behaviors/communications/http/url/endpoint::'
expected = {
    'graph-collection-url.js': {
        prefix + 'group-collection-path-token',
        prefix + 'domain-collection-path-token',
        prefix + 'organization-path-token',
    },
    'relative-module-require.js': set(),
}
for fixture in sorted(Path(__file__).parent.glob('*.js')):
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
    endpoint = {t['id'] for t in traits if t['id'].startswith(prefix)}
    assert endpoint == expected[fixture.name], (fixture.name, sorted(endpoint))
    print(f'{fixture.name}: passed')
