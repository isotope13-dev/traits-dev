#!/usr/bin/env python3
"""Exercise the DEX socket, command and SMS call-cluster rule."""
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
    'no-socket': (b'Ljava/net/Socket;', b'Ljava/net/Sockex;'),
    'no-executor': (b'Executer', b'Executex'),
    'no-sms-helper': (b'sendSMS', b'sendSMX'),
    'no-runtime': (b'Ljava/lang/Runtime;', b'Ljava/lang/Runtimx;'),
    'no-sms-api': (b'Landroid/telephony/SmsManager;', b'Landroid/telephony/SmsManagex;'),
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
        assert ('android-socket-command-sms-tasking-cluster' in ids) == report['path'].endswith('/positive.dex'), report['path']
print('Socket tasking rule rejects five missing call components')
