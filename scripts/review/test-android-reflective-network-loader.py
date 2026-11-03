#!/usr/bin/env python3
"""Exercise combined Android reflective loader and component clues."""
import hashlib
import json
import os
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import zlib

root = Path(__file__).resolve().parents[2]
cleave = os.environ.get('CLEAVE', str(root.parent / 'cleave/target/release/cleave'))
source = Path(sys.argv[1]).read_bytes()
changes = {
    'no-parent': (b'parent\x00', b'pareny\x00'),
    'no-component': (b'getComponentName', b'getComponentNamx'),
    'no-dex-loader': (b'DexClassLoader', b'DexClassLoadex'),
    'no-local-socket': (b'LocalServerSocket', b'LocalServerSockex'),
    'no-url': (b'Ljava/net/URL;', b'Ljava/net/URX;'),
    'no-stage-name': (b'main.apk', b'main.apx'),
    'no-boot': (b'BOOT_COMPLETED', b'BOOT_COMPLETEY'),
}
with tempfile.TemporaryDirectory() as directory:
    paths = []
    for name, change in [('positive', None), *changes.items()]:
        data = source
        if change:
            old, new = change
            assert len(old) == len(new) and old in data, name
            data = data.replace(old, new)
        data = bytearray(data)
        data[12:32] = hashlib.sha1(data[32:]).digest()
        struct.pack_into('<I', data, 8, zlib.adler32(data[12:]) & 0xffffffff)
        path = Path(directory) / (name + '.dex')
        path.write_bytes(data)
        paths.append(str(path))
    result = subprocess.run([cleave, '--traits-dir', str(root), '--json', *paths],
                            capture_output=True, text=True, check=True,
                            env={**os.environ, 'CLEAVE_SKIP_CACHE': '1'})
    rows = [json.loads(line) for line in result.stdout.split('\n') if line]
    assert len(rows) == len(paths)
    for row in rows:
        report = row['files'][0]
        ids = {t['id'].split('::')[-1] for t in report.get('traits', [])}
        assert ('android-reflective-network-loader-component-disable' in ids) == report['path'].endswith('/positive.dex'), report['path']
print('Reflective loader rule rejects seven missing evidence components')
