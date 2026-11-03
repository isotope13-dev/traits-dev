#!/usr/bin/env python3
"""Exercise APK path-poisoning evidence with modified archive members."""
from copy import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from zipfile import ZipFile

root = Path(__file__).resolve().parents[2]
cleave = os.environ.get('CLEAVE', str(root.parent / 'cleave/target/release/cleave'))
source = Path(sys.argv[1])
with tempfile.TemporaryDirectory() as directory, ZipFile(source) as original:
    paths = []
    for name in ('positive', 'no-manifest-parent', 'no-dex-parent', 'no-unsafe-path'):
        path = Path(directory) / (name + '.apk')
        with ZipFile(path, 'w') as output:
            for entry in original.infolist():
                info = copy(entry)
                if name == 'no-manifest-parent':
                    info.filename = info.filename.replace('AndroidManifest.xml/', 'OtherManifest.xml/')
                elif name == 'no-dex-parent':
                    info.filename = info.filename.replace('classes.dex/', 'other-dex/')
                elif name == 'no-unsafe-path':
                    info.filename = info.filename.lstrip('/')
                output.writestr(info, original.read(entry))
        paths.append(str(path))
    result = subprocess.run([cleave, '--traits-dir', str(root), '--json', *paths],
                            capture_output=True, text=True, check=True,
                            env={**os.environ, 'CLEAVE_SKIP_CACHE': '1'})
    rows = [json.loads(line) for line in result.stdout.split('\n') if line]
    assert len(rows) == len(paths)
    for row in rows:
        report = row['files'][0]
        ids = {t['id'].split('::')[-1] for t in report.get('traits', [])}
        assert ('apk-unsafe-manifest-dex-parent-paths' in ids) == report['path'].endswith('/positive.apk'), report['path']
print('Poisoned APK rule rejects missing manifest, DEX or unsafe paths')
