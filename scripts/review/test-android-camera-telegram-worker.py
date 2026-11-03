#!/usr/bin/env python3
"""Check Android camera-directory and fixed-bot worker evidence."""
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
changes = {
    'no-public-directory': (b'getExternalStoragePublicDirectory', b'getExternalStoragePublicDirectorx'),
    'no-list': (b'listFiles', b'listFilex'),
    'no-photo-helper': (b'sendPhotoToTelegram', b'sendPhotoToTelegrax'),
    'no-periodic-work': (b'enqueueUniquePeriodicWork', b'enqueueUniquePeriodicWorx'),
    'no-camera': (b'Camera\x00', b'Camerx\x00'),
    'no-photo-path': (b'/sendPhoto', b'/sendPhotx'),
}
with tempfile.TemporaryDirectory() as directory:
    paths = []
    for name in ['positive', *changes, 'no-bot-token']:
        data = source
        if name in changes:
            old, new = changes[name]
            assert len(old) == len(new) and old in data, name
            data = data.replace(old, new)
        elif name == 'no-bot-token':
            data, count = re.subn(rb'([0-9]{8,12}):([A-Za-z0-9_-]{30,60})', rb'\1!\2', data)
            assert count
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
        assert ('android-camera-telegram-periodic-photo-clues' in ids) == report['path'].endswith('/positive.dex'), report['path']
print('Camera Telegram worker rule rejects seven missing evidence components')
