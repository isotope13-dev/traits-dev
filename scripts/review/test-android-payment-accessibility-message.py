#!/usr/bin/env python3
"""Check Android accessibility-message and payment-package evidence."""
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
    'no-event': [(b'AccessibilityRecord;', b'AccessibilityRecorx;')],
    'no-message': [(b'publishRemoteMessage', b'publishRemoteMessagx')],
    'no-json': [(b'Lorg/json/JSONObject;', b'Lorg/json/JSONObjecx;')],
    'no-password': [(b'isPassword', b'isPasswore')],
    'one-payment-app': [(b'com.phonepe.app', b'com.phonepx.app'),
                        (b'co.id.bankbsi.superapp', b'co.id.bankbsx.superapp')],
}
with tempfile.TemporaryDirectory() as directory:
    paths = []
    for name, edits in [('positive', []), *changes.items()]:
        data = source
        for old, new in edits:
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
        assert ('android-payment-accessibility-remote-message-clues' in ids) == report['path'].endswith('/positive.dex'), report['path']
print('Accessibility payment-message rule rejects five missing evidence components')
