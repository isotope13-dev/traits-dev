#!/usr/bin/env python3
"""CKEditor dialog registration fires only on the parsed CKEDITOR call.

Run `python3 testdata/ckeditor-dialog-identity/check.py <scratch>`.
Fixtures are copied outside testdata so path suppressors cannot mask them.
"""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

TRAIT = 'well-known/lib/ui/ckeditor/dialog::ckeditor-dialog-registration'
expected = {
    'positive-dialog.js': True,
    'negative-other-dialog.js': False,
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
