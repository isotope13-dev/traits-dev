#!/usr/bin/env python3
"""Private manifests are not published-package traversal risks (see README).

Run `python3 testdata/npm-main-private/check.py <scratch-directory>`.
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

RULE = ('objectives/supply-chain/install-hook/package/manifest::'
        'npm-main-parent-entrypoint')
expected = {
    'negative': False,
    'positive': True,
}

scratch = Path(sys.argv[1])
scratch.mkdir(parents=True, exist_ok=True)
root = Path(__file__).resolve().parents[2]
for name, want in sorted(expected.items()):
    target = scratch / name / 'package.json'
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(Path(__file__).parent / name / 'package.json', target)
    result = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(root),
         '--format', 'json', str(target)],
        env=dict(os.environ, CLEAVE_VALIDATE='0'), text=True,
        capture_output=True, check=True,
    )
    report = json.loads(result.stdout)
    seen = {t['id'] for e in report['files'] for t in e.get('traits', [])}
    got = RULE in seen
    assert got == want, (name, sorted(seen))
    print(f'{name}/package.json: passed')
