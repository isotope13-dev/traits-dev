#!/usr/bin/env python3
"""Check that the SMS record and command finding requires its evidence."""
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
changes = {
    'no-phone-setter': (b'setPhone', b'setPhonx'),
    'no-content-setter': (b'setContent', b'setContenx'),
    'no-list-adder': (b'addSmsList', b'addSmsLisx'),
    'no-delete-command': (b'DELETE_SMS', b'DELETE_SMX'),
    'no-send-command': (b'SEND_SMS', b'SEND_SMX'),
    'no-app-list-command': (b'GET_APP_LIST', b'GET_APP_LISX'),
    'no-sms-uri': (b'content://sms/', b'content://smx/'),
}
def checksum(data):
    data = bytearray(data)
    data[12:32] = hashlib.sha1(data[32:]).digest()
    struct.pack_into('<I', data, 8, zlib.adler32(data[12:]) & 0xffffffff)
    return data
with tempfile.TemporaryDirectory() as directory, ZipFile(sys.argv[1]) as original:
    paths = []
    for name in ('positive', *changes, 'no-sms-permission'):
        path = Path(directory) / (name + '.apk')
        changed = 0
        with ZipFile(path, 'w') as output:
            for entry in original.infolist():
                data = original.read(entry)
                if name in changes and entry.filename.startswith('classes') and entry.filename.endswith('.dex'):
                    old, new = changes[name]
                    assert len(old) == len(new)
                    changed += data.count(old)
                    if old in data:
                        data = checksum(data.replace(old, new))
                if name == 'no-sms-permission' and entry.filename == 'AndroidManifest.xml':
                    old = 'android.permission.READ_SMS'.encode('utf-16le')
                    new = 'android.permission.READ_SMX'.encode('utf-16le')
                    changed += data.count(old)
                    data = data.replace(old, new)
                output.writestr(copy(entry), data)
        assert name == 'positive' or changed, name
        paths.append(str(path))
    result = subprocess.run([cleave, '--traits-dir', str(root), '--json', *paths],
                            capture_output=True, text=True, check=True,
                            env={**os.environ, 'CLEAVE_SKIP_CACHE': '1', 'RAYON_NUM_THREADS': '2'})
    rows = [json.loads(line) for line in result.stdout.split('\n') if line]
    assert len(rows) == len(paths)
    for row in rows:
        f = row['files'][0]
        ids = {t['id'].split('::')[-1] for t in f.get('traits', [])}
        assert ('android-sms-records-with-remote-command-clues' in ids) == f['path'].endswith('/positive.apk'), f['path']
print('SMS record and command rule rejects eight missing evidence components')
