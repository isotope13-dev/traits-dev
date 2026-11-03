#!/usr/bin/env python3
"""Check compiled AppleScript build-stage evidence independently."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

root = Path(__file__).resolve().parents[2]
cleave = os.environ.get('CLEAVE', str(root.parent / 'cleave/target/release/cleave'))
source = Path(sys.argv[1]).read_bytes()
changes = {
    'no-compile': ('osacompile', 'osacompilx'),
    'no-vendor': ('build_vendor', 'build_vendox'),
    'no-version': ('build_version', 'build_versiox'),
    'no-framework': ('CoreFrameworks', 'CoreFrameworkx'),
}
with tempfile.TemporaryDirectory() as directory:
    paths = []
    for name in ('positive', *changes):
        data = source
        if name in changes:
            old, new = changes[name]
            changed = 0
            for encoding in ('utf-8', 'utf-16le', 'utf-16be'):
                a, b = old.encode(encoding), new.encode(encoding)
                changed += data.count(a)
                data = data.replace(a, b)
            assert changed, name
        path = Path(directory) / (name + '.scpt')
        path.write_bytes(data)
        paths.append(str(path))
    result = subprocess.run([cleave, '--traits-dir', str(root), '--json', *paths],
                            capture_output=True, text=True, check=True,
                            env={**os.environ, 'CLEAVE_SKIP_CACHE': '1'})
    for line in result.stdout.split('\n'):
        if line:
            f = json.loads(line)['files'][0]
            match = any(t['id'].endswith('::compiled-build-tagged-remote-script-stage') for t in f.get('traits', []))
            assert match == f['path'].endswith('/positive.scpt'), f['path']
print('Compiled AppleScript build-stage rule rejects four controls')
