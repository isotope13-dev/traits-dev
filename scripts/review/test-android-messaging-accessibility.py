#!/usr/bin/env python3
"""Check cross-app accessibility message-view call evidence."""
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
    'no-whatsapp-view': (b'com.whatsapp:id/message_text', b'com.whatsapp:id/message_texx'),
    'no-viber-view': (b'com.viber.voip:id/textMessageView', b'com.viber.voip:id/textMessageViex'),
    'no-text-read': (b'getText\x00', b'getTexx\x00'),
}
with tempfile.TemporaryDirectory() as directory:
    paths = []
    for name, edit in [('positive', None), *changes.items()]:
        data = source
        if edit:
            old, new = edit
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
        assert ('android-accessibility-multiple-message-views' in ids) == report['path'].endswith('/positive.dex'), report['path']
print('Messaging accessibility rule rejects three missing call components')
