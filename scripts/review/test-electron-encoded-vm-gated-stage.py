#!/usr/bin/env python3
"""Verify encoded VM-gated PowerShell facts and obfuscator context."""
import base64
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
root = Path(__file__).resolve().parents[2]
cleave = os.environ.get('CLEAVE', str(root.parent / 'cleave/target/release/cleave'))
source = Path(sys.argv[1]).read_text()
encoded = max(re.findall(r'[A-Za-z0-9+/]{120,}={0,2}', source), key=len)
payload = base64.b64decode(encoded, validate=True)
changes = {
    'no-processor': (b'Win32_Processor', b'Win32_Prozessox'),
    'no-system': (b'Win32_ComputerSystem', b'Win32_ComputerSystex'),
    'no-video': (b'Win32_VideoController', b'Win32_VideoControllxx'),
    'no-core-count': (b'NumberOfLogicalProcessors', b'NumberOfLogicalProcessoxx'),
    'no-vmware': (b'vmware', b'vmwarx'),
    'no-eval': (b' | iex', b' | out'),
}
with tempfile.TemporaryDirectory() as directory:
    paths = []
    for name in ('positive', *changes, 'no-obfuscator'):
        data = source
        if name in changes:
            old, new = changes[name]
            assert len(old) == len(new) and old in payload, name
            data = source.replace(encoded, base64.b64encode(payload.replace(old, new)).decode())
        elif name == 'no-obfuscator':
            data = "const payload = '" + encoded + "';\n"
        path = Path(directory) / (name + '.js')
        path.write_text(data)
        paths.append(str(path))
    result = subprocess.run([cleave, '--traits-dir', str(root), '--json', *paths],
                            capture_output=True, text=True, check=True,
                            env={**os.environ, 'CLEAVE_SKIP_CACHE': '1'})
    rows = [json.loads(line) for line in result.stdout.split('\n') if line]
    assert len(rows) == len(paths)
    for row in rows:
        f = row['files'][0]
        match = any(t['id'].endswith('::obfuscated-electron-vm-gated-powershell-stage') for t in f.get('traits', []))
        assert match == f['path'].endswith('/positive.js'), f['path']
print('Encoded VM-gated stage rejects seven missing-evidence controls')
