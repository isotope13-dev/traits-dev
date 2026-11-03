#!/usr/bin/env python3
"""Exercise the Nuitka RAT rule against a specimen and mutated copies."""

import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

root = Path(__file__).resolve().parents[2]
cleave = os.environ.get('CLEAVE', str(root.parent / 'cleave/target/release/cleave'))
source = Path(sys.argv[1]).read_bytes()
patterns = {
    'no-hide': b'attrib +s +h %localappdata%\\',
    'no-registry': b'REG ADD HKEY_LOCAL_MACHINE\\Software\\Microsoft\\Windows\\CurrentVersion\\Run',
    'no-socket': b'websockets.client',
    'no-screen': b'screenshot',
    'no-upload': b'AnonFiles',
    'no-task': b'COMMAND',
}
with tempfile.TemporaryDirectory() as directory:
    paths = []
    positive = Path(directory) / 'positive.exe'
    positive.write_bytes(source)
    paths.append(str(positive))
    for name, pattern in patterns.items():
        assert pattern in source, name
        path = Path(directory) / (name + '.exe')
        path.write_bytes(re.sub(re.escape(pattern), b'X' * len(pattern), source, flags=re.I))
        paths.append(str(path))
    result = subprocess.run([cleave, '--traits-dir', str(root), '--json', *paths],
                            capture_output=True, text=True, check=True,
                            env={**os.environ, 'CLEAVE_SKIP_CACHE': '1'})
    rows = [json.loads(line) for line in result.stdout.split('\n') if line]
    assert len(rows) == len(paths)
    for row in rows:
        report = row['files'][0]
        matched = any(t['id'].endswith('::nuitka-hidden-persistence-tasking')
                      for t in report.get('traits', []))
        assert matched == report['path'].endswith('/positive.exe'), report['path']
print('Nuitka RAT rule rejects missing persistence, socket, capture, upload and task clues')
