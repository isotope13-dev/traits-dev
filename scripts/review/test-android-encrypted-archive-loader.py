#!/usr/bin/env python3
"""Check encrypted-archive loader evidence in DEX and APK controls."""
from copy import copy
import hashlib
import json
import os
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
from zipfile import ZipFile
import zlib

root = Path(__file__).resolve().parents[2]
cleave = os.environ.get('CLEAVE', str(root.parent / 'cleave/target/release/cleave'))
source = Path(sys.argv[1])
changes = {
    'no-cipher': (b'CipherInputStream', b'CipherInputStreax'),
    'no-zip': (b'ZipInputStream', b'ZipInputStreax'),
    'no-file-output': (b'FileOutputStream', b'FileOutputStreax'),
    'no-reflection': (b'getDeclaredMethod', b'getDeclaredMethox'),
}

def checksum(data):
    data = bytearray(data)
    data[12:32] = hashlib.sha1(data[32:]).digest()
    struct.pack_into('<I', data, 8, zlib.adler32(data[12:]) & 0xffffffff)
    return data

with tempfile.TemporaryDirectory() as directory, ZipFile(source) as original:
    paths = []
    for name in ('positive', *changes, 'no-phone', 'no-opaque-asset'):
        path = Path(directory) / (name + '.apk')
        with ZipFile(path, 'w') as output:
            for entry in original.infolist():
                info = copy(entry)
                data = original.read(entry)
                if name in changes and entry.filename == 'classes2.dex':
                    old, new = changes[name]
                    assert len(old) == len(new) and old in data, name
                    data = checksum(data.replace(old, new))
                if name == 'no-phone' and entry.filename == 'AndroidManifest.xml':
                    old = 'android.permission.CALL_PHONE'.encode('utf-16le')
                    new = 'android.permission.CALL_PHONX'.encode('utf-16le')
                    assert old in data
                    data = data.replace(old, new)
                if name == 'no-opaque-asset' and info.filename == 'assets/kdcnbw':
                    info.filename += '.bin'
                output.writestr(info, data)
        paths.append(str(path))
    result = subprocess.run([cleave, '--traits-dir', str(root), '--json', *paths],
                            capture_output=True, text=True, check=True,
                            env={**os.environ, 'CLEAVE_SKIP_CACHE': '1', 'RAYON_NUM_THREADS': '2'})
    rows = [json.loads(line) for line in result.stdout.split('\n') if line]
    assert len(rows) == len(paths)
    for row in rows:
        report = row['files'][0]
        ids = {t['id'].split('::')[-1] for t in report.get('traits', [])}
        assert ('android-opaque-encrypted-archive-loader-call-access' in ids) == report['path'].endswith('/positive.apk'), report['path']
print('Encrypted archive loader rule rejects six missing evidence components')
