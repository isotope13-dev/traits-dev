#!/usr/bin/env python3
"""Exercise lock-screen recording evidence with size-preserving DEX edits."""
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
    'no-lock-detection': [(b'detectLockScreenType', b'detectLockScreenTypx')],
    'no-recording': [(b'StartRecording', b'StartRecordinx')],
    'no-touch-x': [(b'getX\x00', b'getZ\x00')],
    'no-touch-y': [(b'getY\x00', b'getZ\x00')],
    'no-pattern': [(b'LockPatternView', b'LockPatternViex'), (b'pattern_view', b'pattern_viex')],
}
with tempfile.TemporaryDirectory() as directory:
    paths = []
    for name, edits in [('positive', []), *changes.items()]:
        data = source
        changed = 0
        for old, new in edits:
            assert len(old) == len(new)
            changed += data.count(old)
            data = data.replace(old, new)
        assert name == 'positive' or changed, name
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
        assert ('android-lockscreen-input-recording' in ids) == report['path'].endswith('/positive.dex'), report['path']
print('Lock-screen recording rule rejects five missing evidence components')
