#!/usr/bin/env python3
"""XOR syntax requires code operands, not translated punctuation.

Run `python3 testdata/xor-syntax-operands/check.py <scratch>`.
Fixtures are copied outside testdata so path suppressors cannot mask them.
"""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

TRAIT = 'micro-behaviors/data/arithmetic::non-python-xor-syntax'
expected = {
    'positive-xor.js': True,
    'negative-translated-caret.js': False,
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
