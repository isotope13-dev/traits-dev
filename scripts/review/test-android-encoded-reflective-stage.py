#!/usr/bin/env python3
"""Exercise encoded/reflection staging clues with preserved-size DEX edits."""
import hashlib
import json
import os
from pathlib import Path
import re
import struct
import subprocess
import sys
import tempfile
import zlib

root = Path(__file__).resolve().parents[2]
cleave = os.environ.get('CLEAVE', str(root.parent / 'cleave/target/release/cleave'))
source = Path(sys.argv[1]).read_bytes()
names = (
    b'c34o56u7897n7865t3435', b'c4356l457o6s8ei6878T6i5m898e87',
    b'c5h67a56n75E67a56n7b56l7e56', b'g5e67t6F7B76876A8p76k8',
    b'o345n654E637n3456te46r573A534c567763t565i32vi542ty', b't3i45m34e534',
)
changes = {
    'no-decode': (b'Landroid/util/Base64;', b'Landroid/util/Base6x;'),
    'no-create': (b'createNewFile', b'createNewFilx'),
    'no-lookup': (b'getDeclaredMethod', b'getDeclaredMethox'),
    'no-constructor': (b'Ljava/lang/reflect/Constructor;', b'Ljava/lang/reflect/Constructox;'),
    'no-invoke': (b'Ljava/lang/reflect/Method;', b'Ljava/lang/reflect/Methox;'),
}
def checksum(data):
    data = bytearray(data)
    data[12:32] = hashlib.sha1(data[32:]).digest()
    struct.pack_into('<I', data, 8, zlib.adler32(data[12:]) & 0xffffffff)
    return data

with tempfile.TemporaryDirectory() as directory:
    paths = []
    for name in ['positive', *changes, 'no-encoded', 'no-mangled']:
        data = source
        if name in changes:
            old, new = changes[name]
            assert len(old) == len(new) and old in data, name
            data = data.replace(old, new)
        elif name == 'no-encoded':
            match = re.search(rb'[A-Za-z0-9+/]{50000,}={0,2}', data)
            assert match
            data = bytearray(data)
            for offset in range(match.start() + 20000, match.end(), 20000):
                data[offset] = ord('!')
        elif name == 'no-mangled':
            for old in names:
                assert old in data
                data = data.replace(old, re.sub(rb'[0-9]', b'x', old))
        path = Path(directory) / (name + '.dex')
        path.write_bytes(checksum(data))
        paths.append(str(path))
    result = subprocess.run([cleave, '--traits-dir', str(root), '--json', *paths],
                            capture_output=True, text=True, check=True,
                            env={**os.environ, 'CLEAVE_SKIP_CACHE': '1'})
    rows = [json.loads(line) for line in result.stdout.split('\n') if line]
    assert len(rows) == len(paths)
    for row in rows:
        report = row['files'][0]
        ids = {t['id'].split('::')[-1] for t in report.get('traits', [])}
        assert ('android-encoded-reflective-stage-obfuscation' in ids) == report['path'].endswith('/positive.dex'), report['path']
print('Encoded reflection rule rejects seven missing evidence components')
