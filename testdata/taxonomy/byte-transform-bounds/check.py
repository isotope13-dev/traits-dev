#!/usr/bin/env python3
"""Exercise register variants and executable-section bounds on tiny PE fixtures."""
import pathlib
import re
import struct
import subprocess
import sys
import tempfile

ARITH = 'micro-behaviors/data/arithmetic::x64-index-scaled-byte-subtraction-loop'
SWAP = 'micro-behaviors/data/reassembly::x64-adjacent-byte-pair-swap-loop'
OLD_ARITH = bytes.fromhex('0F B6 14 01 48 89 CB 48 C1 E3 05 48 29 CB 29 DA 83 C2 F5 88 14 08 48 FF C1 48 81 F9 00 00 01 00 7C DB')
OLD_SWAP = bytes.fromhex('0F B6 5C 10 01 0F B6 34 10 88 1C 02 40 88 74 10 01 48 83 C0 02 48 8D 58 01 48 81 FB 00 00 01 00 7D 0D')
NEW_ARITH = bytes.fromhex('44 0F B6 04 10 4C 8D 0C 40 4E 8D 0C 48 45 29 C8 41 83 C0 7C 44 88 04 02 48 FF C0 48 3D 00 00 01 00 7C DD')
NEW_SWAP = bytes.fromhex('44 0F B6 44 10 01 44 0F B6 0C 10 44 88 04 02 44 88 4C 10 01 48 83 C0 02')


def image(code, data=b''):
    buf = bytearray(1536)
    buf[:2] = b'MZ'
    struct.pack_into('<I', buf, 0x3c, 0x80)
    buf[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', buf, 0x84, 0x8664, 2, 0, 0, 0, 240, 0x22)
    opt = 0x98
    struct.pack_into('<H', buf, opt, 0x20b)
    struct.pack_into('<II', buf, opt + 16, 0x1000, 0x1000)
    struct.pack_into('<QII', buf, opt + 24, 0x140000000, 4096, 512)
    struct.pack_into('<II', buf, opt + 56, 0x3000, 512)
    struct.pack_into('<H', buf, opt + 68, 3)
    struct.pack_into('<I', buf, opt + 108, 16)
    for k, (name, va, off, flags) in enumerate([
        (b'.text', 0x1000, 512, 0x60000020),
        (b'.rdata', 0x2000, 1024, 0x40000040),
    ]):
        pos = opt + 240 + k * 40
        struct.pack_into('<8sIIIIIIHHI', buf, pos, name, 512, va, 512, off, 0, 0, 0, 0, flags)
    buf[512:512 + len(code)] = code
    buf[1024:1024 + len(data)] = data
    return buf


cases = [
    ('old-registers', image(OLD_ARITH + OLD_SWAP), {ARITH, SWAP}),
    ('new-registers', image(NEW_ARITH + NEW_SWAP), {ARITH, SWAP}),
    ('alternate-scale', image(NEW_ARITH.replace(b'\x0c\x48', b'\x0c\x88') + NEW_SWAP), {ARITH, SWAP}),
    ('arithmetic-only', image(NEW_ARITH), {ARITH}),
    ('swap-only', image(NEW_SWAP), {SWAP}),
    ('non-code-decoy', image(b'\xc3', NEW_ARITH + NEW_SWAP), set()),
]
engine = sys.argv[1] if len(sys.argv) > 1 else 'cleave'
with tempfile.TemporaryDirectory(prefix='.controls-', dir=pathlib.Path(__file__).parent) as temp:
    for name, buf, expected in cases:
        path = pathlib.Path(temp, name + '.exe')
        path.write_bytes(buf)
        result = subprocess.run([engine, '--traits-dir', '.', 'test-rules', str(path), '--rules', ARITH + ',' + SWAP], capture_output=True, text=True)
        output = result.stdout + result.stderr
        actual = {rule for rule in [ARITH, SWAP] if re.search(r'^MATCHED ' + re.escape(rule) + r' \(trait\)', output, re.M)}
        if result.returncode or actual != expected or 'validation failed' in output:
            raise SystemExit(f'{name}: expected {expected}, got {actual}\n{output}')
        print(name + ': passed')
