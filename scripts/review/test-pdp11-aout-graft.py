#!/usr/bin/env python3
"""Test a.out entry binding and instruction-pattern negatives without execution."""
import json
import os
from pathlib import Path
import struct
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave'))
RULE = 'objectives/impact/infect/binary/unix-aout::pdp11-appended-entry-aout-infector'
ENTRY = bytes.fromhex('C3 11 E6 28 C4 10 C4 65 BC 00 11 15 11 15 C5 15 77 00')
PATCH = bytes.fromhex('CC 25 07 01 24 02 80 14 80 62 40 E0 D2 65 C0 00 D2 65 2E 00 D2 0B')
APPEND = bytes.fromhex('80 13 13 89 00 00 02 00 80 13 04 89 04 00 C0 00')
REWRITE = bytes.fromhex('80 13 13 89 00 00 00 00 80 13 04 89 C4 00 14 00')

def fixture():
    b = bytearray(512)
    for at, value in [(0, 0o407), (2, 200), (4, 296), (14, 1), (16, 0o167), (18, 216)]:
        struct.pack_into('<H', b, at, value)
    start = 16 + 220
    for offset, code in [(0, ENTRY), (32, PATCH), (72, APPEND), (100, REWRITE)]:
        b[start+offset:start+offset+len(code)] = code
    return bytes(b)

def matches(data):
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / 'image.bin'
        path.write_bytes(data)
        proc = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), '--format=json', str(path)],
                              check=True, capture_output=True, text=True,
                              env={**os.environ, 'CLEAVE_SKIP_CACHE': '1'})
        return any(t['id'] == RULE for f in json.loads(proc.stdout)['files'] for t in f.get('traits', []))

source = fixture()
assert matches(source)
for old in [ENTRY, PATCH, APPEND, REWRITE]:
    assert not matches(source.replace(old, b'\0' * len(old))), old.hex()
for at, value in [(0, 0), (14, 0), (16, 0), (18, 0)]:
    b = bytearray(source)
    b[at] = value
    assert not matches(bytes(b)), at
# A jump to the same byte sequence while the text section contains it is not
# the documented jump into initialized data.
b = bytearray(source)
struct.pack_into('<H', b, 2, 240)
struct.pack_into('<H', b, 4, 256)
assert not matches(bytes(b))
print('PDP-11 graft rule binds the a.out entry and requires each file-write sequence')
