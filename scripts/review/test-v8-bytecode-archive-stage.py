#!/usr/bin/env python3
"""Check archive-stage facts in a compiled JavaScript data member."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from zipfile import ZipFile
root = Path(__file__).resolve().parents[2]
cleave = os.environ.get('CLEAVE', str(root.parent / 'cleave/target/release/cleave'))
source = Path(sys.argv[1]).read_bytes()
changes = {
    'no-url': (b'https://deliverynetwork.observer/qfast/AdditionalFilesForMeet.zip', b'htxps://deliverynetwork.observer/qfast/AdditionalFilesForMeet.zip'),
    'no-file-stream': (b'createWriteStream', b'createWriteStreax'),
    'no-extract': (b'extractAllTo', b'extractAllTx'),
    'no-tempdir': (b'mkdtempSync', b'mkdtempSynx'),
    'no-start-process': (b'powershell Start-Process ', b'powershell Start-Procesx '),
    'no-elevation': (b'-Verb runAs', b'-Verb runAx'),
    'no-child-process': (b'child_process', b'child_procesx'),
}
with tempfile.TemporaryDirectory() as directory:
    paths = []
    for name in ('positive', *changes, 'no-bytecode-extension'):
        data = source
        if name in changes:
            old, new = changes[name]
            assert len(old) == len(new) and old in data, name
            data = data.replace(old, new)
        member = 'out/main/index.jsc' if name != 'no-bytecode-extension' else 'out/main/index.bin'
        path = Path(directory) / (name + '.zip')
        with ZipFile(path, 'w') as z:
            z.writestr(member, data)
        paths.append(str(path))
    result = subprocess.run([cleave, '--all-files', '--traits-dir', str(root), '--json', *paths],
                            capture_output=True, text=True, check=True,
                            env={**os.environ, 'CLEAVE_SKIP_CACHE': '1', 'RAYON_NUM_THREADS': '2'})
    rows = [json.loads(line) for line in result.stdout.split('\n') if line]
    assert len(rows) == len(paths)
    for row in rows:
        f = row['files'][0]
        match = any(t['id'].endswith('::jsc-compiled-remote-archive-elevation') for t in f.get('traits', []))
        assert match == f['path'].endswith('/positive.zip'), f['path']
print('Compiled JavaScript archive-stage rule rejects eight controls')
