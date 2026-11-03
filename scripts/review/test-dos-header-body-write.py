#!/usr/bin/env python3
"""Find a DOS executable search with a three-byte patch and body write."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave'))
RULE = 'objectives/impact/infect/binary/dos/file::dos-searched-header-and-image-write'
# A synthetic instruction stream: find-first, seek start, three-byte write,
# a near call, and a second write sized using the COM load address.
FIND = bytes.fromhex('b4 4e b9 00 00 8d 56 2b cd 21')
SEEK = bytes.fromhex('b8 00 42 8b 5e 3f 33 c9 cd 21')
WRITE = bytes.fromhex('b4 40 8b 5e 3f b9 03 00 8d 56 46 cd 21 8b 56 47 83 c2 03 e8 65 01 b4 40 8b 5e 3f 8d 0e 2c 05 8d 16 00 01 2b ca 8d 56 fa cd 21')
PREFIX = bytes.fromhex('e9 00 00') + b'*.COM\x00'
cases = [
    ('all', PREFIX + FIND + SEEK + WRITE, True),
    ('four_bytes', PREFIX + FIND + SEEK + WRITE.replace(bytes.fromhex('b9 03 00'), bytes.fromhex('b9 04 00')), False),
    ('no_search', PREFIX + SEEK + WRITE, False),
    ('no_mask', bytes.fromhex('e9 00 00') + FIND + SEEK + WRITE, False),
    ('no_second_write', PREFIX + FIND + SEEK + WRITE[:-3], False),
]
with tempfile.TemporaryDirectory() as tmp:
    for name, payload, expected in cases:
        path = Path(tmp) / (name + '.com')
        path.write_bytes(payload.ljust(512, b'\x90'))
        proc = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), '--all-files', '--format=json', str(path)],
                              check=True, capture_output=True, text=True,
                              env={**os.environ, 'CLEAVE_SKIP_CACHE': '1'})
        found = any(t['id'] == RULE for f in json.loads(proc.stdout)['files'] for t in f.get('traits', []))
        assert found == expected, (name, found)
print('DOS executable search and header/body-write boundaries passed')
