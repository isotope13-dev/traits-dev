#!/usr/bin/env python3
"""Check isolated primitives and dependency-removal controls without execution.
Usage: python3 check.py /absolute/path/to/the/Go/sample.exe
"""
import json
import os
from pathlib import Path
import struct
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', 'cleave')
UNPACK = 'objectives/anti-static/pack/manual-map::go-arithmetic-pe-unpacker'
SUBST = 'objectives/evasion/process/loader::go-packed-pe-imagebase-substitution'
ARITH = 'micro-behaviors/data/arithmetic::x64-index-scaled-byte-subtraction-loop'
ENTRY = 'micro-behaviors/data/arithmetic::go-field-base-sum-call-setup'
PEB = 'micro-behaviors/mem/write/arbitrary::x64-pointer-60-field-10-store'
SOCKS = 'micro-behaviors/communications/proxy/socks::socks5-noauth-greeting-stack-store-x86-64'

def scan(path):
    r = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), '--format', 'json', str(path)],
                       capture_output=True, text=True, check=True)
    j = json.loads(r.stdout)
    return {t['id']: t for f in j['files'] for t in f.get('traits', [])}

def pe64(code):
    """Inert PE container: entry returns; patterns are unreachable bytes."""
    b = bytearray(1024)
    b[:2] = b'MZ'
    struct.pack_into('<I', b, 0x3c, 0x80)
    b[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', b, 0x84, 0x8664, 1, 0, 0, 0, 240, 0x22)
    struct.pack_into('<H', b, 0x98, 0x20b)
    struct.pack_into('<I', b, 0x98+16, 0x1000)
    struct.pack_into('<Q', b, 0x98+24, 0x140000000)
    struct.pack_into('<II', b, 0x98+32, 0x1000, 0x200)
    struct.pack_into('<II', b, 0x98+56, 0x2000, 0x200)
    struct.pack_into('<H', b, 0x98+68, 3)
    struct.pack_into('<I', b, 0x98+108, 16)
    b[0x188:0x190] = b'.text\0\0\0'
    struct.pack_into('<IIII', b, 0x190, 512, 0x1000, 512, 512)
    struct.pack_into('<I', b, 0x1ac, 0x60000020)
    b[512:512+len(code)+1] = b'\xc3'+code
    return b


def elf32(code):
    b = bytearray(0x300)
    b[:16] = b'\x7fELF\x01\x01\x01' + bytes(9)
    struct.pack_into('<HHIIIIIHHHHHH', b, 16, 2, 3, 1, 0x8048100, 0, 0x200, 0,
                     52, 0, 0, 40, 3, 2)
    names = b'\0.text\0.shstrtab\0'
    b[0x180:0x180+len(names)] = names
    b[0x100:0x100+len(code)+1] = b'\xc3'+code
    struct.pack_into('<IIIIIIIIII', b, 0x228, 1, 1, 6, 0x8048100, 0x100,
                     len(code)+1, 0, 0, 16, 0)
    struct.pack_into('<IIIIIIIIII', b, 0x250, 7, 3, 0, 0, 0x180, len(names), 0, 0, 1, 0)
    return b

with tempfile.TemporaryDirectory(prefix='native-rule-controls-') as tmp:
    tmp = Path(tmp)
    for name, code, expect in [
        ('socks-store', bytes.fromhex('66 C7 44 24 20 05 01 C6 44 24 22 00'), True),
        ('socks-byte-collision', bytes.fromhex('05 01 00 05 00 00'), False),
        ('socks-auth-method-near-miss', bytes.fromhex('66 C7 44 24 20 05 02 C6 44 24 22 00'), False),
    ]:
        path = tmp / (name+'.exe')
        path.write_bytes(pe64(code))
        got = scan(path)
        assert (SOCKS in got) == expect, (name, got.keys())
        assert UNPACK not in got and SUBST not in got
        print('PASS', name)
    socket_id = 'micro-behaviors/communications/socket/create::i386-musl-socket-wrapper'
    wrapper = bytes.fromhex('BE 01 00 00 00 53 BB 66 00 00 00') + b'\x90'*12 + bytes.fromhex('89 D8 89 F2 E8 00 00 00 00')
    for name, code, expect in [
        ('socket-trampoline', wrapper, True),
        ('non-socket-operation', wrapper.replace(b'\xbe\x01', b'\xbe\x02'), False),
    ]:
        path = tmp / (name+'.elf')
        path.write_bytes(elf32(code))
        got = scan(path)
        assert (socket_id in got) == expect, name
        print('PASS', name)
    if len(sys.argv) > 1:
        source = Path(sys.argv[1])
        b = source.read_bytes()
        before = scan(source)
        assert UNPACK in before and SUBST in before
        for name, dependency, required, forbidden in [
            ('without-decoder', ARITH, [], [UNPACK, SUBST]),
            ('without-entry-handoff', ENTRY, [], [UNPACK, SUBST]),
            ('without-imagebase-write', PEB, [UNPACK], [SUBST]),
        ]:
            changed = bytearray(b)
            assert dependency in before, dependency
            for start, length in before[dependency]['spans']:
                changed[start] = 0x90
            path = tmp / (name+'.exe')
            path.write_bytes(changed)
            got = scan(path)
            assert dependency not in got
            assert all(x in got for x in required), (name, required)
            assert all(x not in got for x in forbidden), (name, forbidden)
            print('PASS', name)
