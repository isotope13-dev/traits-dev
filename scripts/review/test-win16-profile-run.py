#!/usr/bin/env python3
"""Check argument and relocation binding for the Win16 profile-run rule."""
import json
import os
from pathlib import Path
import struct
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave'))
RULE = 'objectives/persistence/login/startup/winini::win16-windows-run-write'
HIDDEN_RULE = 'objectives/persistence/login/startup/winini::win16-hidden-run-executable'


def fixture(code=0x200, data=0x400, value=b'demo.exe\0'):
    data_size = max(0x80, 0x40 + len(value))
    b = bytearray(max(code + 0x90, data + data_size))
    def put(at, value):
        struct.pack_into('<H', b, at, value)
    b[:2] = b'MZ'
    struct.pack_into('<I', b, 0x3c, 0x40)
    b[0x40:0x42] = b'NE'
    put(0x40+0x0e, 2)
    put(0x40+0x1c, 2)
    put(0x40+0x1e, 1)
    put(0x40+0x22, 0x40)
    put(0x40+0x28, 0x50)
    put(0x40+0x2a, 0x52)
    put(0x40+0x32, 4)
    b[0x40+0x36] = 2
    put(0x80, code >> 4)
    put(0x82, 0x80)
    put(0x84, 0x100)
    put(0x88, data >> 4)
    put(0x8a, data_size)
    b[0x92:0x99] = b'\x06KERNEL'
    b[code+0x20:code+0x31] = bytes.fromhex('1e 68 20 00 1e 68 30 00 1e 68 40 00 9a ff ff 00 00')
    put(code+0x80, 1)
    b[code+0x82:code+0x8a] = bytes.fromhex('03 01 2d 00 01 00 3b 00')
    b[data+0x20:data+0x28] = b'windows\0'
    b[data+0x30:data+0x34] = b'run\0'
    b[data+0x40:data+0x40+len(value)] = value
    return b


def matches(b, rule=RULE):
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / 'sample.exe'
        path.write_bytes(b)
        proc = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), '--format=json', str(path)],
                              check=True, capture_output=True, text=True,
                              env={**os.environ, 'CLEAVE_SKIP_CACHE': '1'})
        return any(t['id'] == rule for f in json.loads(proc.stdout)['files'] for t in f.get('traits', []))

assert matches(fixture())
assert matches(fixture(0x300, 0x500))
for at, value in [(0x430, ord('x')), (0x220+6, 0x40), (0x282+2, 0x2e),
                  (0x282+6, 0x3c), (0x93, ord('X')), (0x40+0x36, 1)]:
    b = fixture()
    b[at] = value
    assert not matches(b), hex(at)
hidden = b' ' * 278 + b'C:\\MSIE5.EXE\0'
assert matches(fixture(value=hidden), HIDDEN_RULE)
assert not matches(fixture(), HIDDEN_RULE)
for value in (b' ' * 63 + b'C:\\MSIE5.EXE\0',
              b' ' * 278 + b'relative.exe\0',
              b' ' * 278 + b'C:\\readme.txt\0'):
    assert not matches(fixture(value=value), HIDDEN_RULE)
for at, value in [(0x430, ord('x')), (0x282 + 2, 0x2e), (0x282 + 6, 0x3c)]:
    b = fixture(value=hidden)
    b[at] = value
    assert not matches(b, HIDDEN_RULE), hex(at)
print('Win16 profile rules bind the call, relocation, and padded executable path')
