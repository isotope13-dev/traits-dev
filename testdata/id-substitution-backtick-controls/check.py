#!/usr/bin/env python3
"""Bare `id` in backticks is a prose field name, not shell substitution.

`micro-behaviors/process/user/query::identity-command-substitution` must not
fire on shell prose (comments) that references a record `id` field in inline
code, while still firing on genuine substitution forms (`` `id -u` ``,
`$(id)`).

Run `python3 testdata/id-substitution-backtick-controls/check.py <scratch>`.
Fixtures are copied outside testdata so path suppressors cannot mask them.
"""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

TRAIT = 'micro-behaviors/process/user/query::identity-command-substitution'
expected = {
    'negative-prose-field.sh': False,
    'positive-id-flag.sh': True,
}

scratch = Path(sys.argv[1])
scratch.mkdir(parents=True, exist_ok=True)
root = Path(__file__).resolve().parents[2]
for fixture, want in sorted(expected.items()):
    target = scratch / fixture
    shutil.copyfile(Path(__file__).parent / fixture, target)
    result = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(root),
         '--format', 'json', str(target)],
        env=dict(os.environ, CLEAVE_VALIDATE='0'), text=True,
        capture_output=True, check=True,
    )
    seen = {t['id'] for e in json.loads(result.stdout)['files']
            for t in e['traits']}
    assert (TRAIT in seen) == want, (fixture, sorted(seen))
    print(f'{fixture}: passed')
