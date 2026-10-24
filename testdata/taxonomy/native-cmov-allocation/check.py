#!/usr/bin/env python3
"""Static PE controls for CMOV dispatch and allocation-call target binding.

No generated code is executed. Run from the traits repository root.
"""
import argparse
import json
from pathlib import Path
import struct
import subprocess
import tempfile

p = argparse.ArgumentParser()
p.add_argument('--record', required=True)
p.add_argument('--atomscan', default='atomscan')
a = p.parse_args()
neutral = 'metadata/binary/code/control-transfer::repeated-cmov-load-add-jump-x64'
flatten = 'objectives/anti-static/obfuscation/control-flow/dispatch::repeated-cmov-relative-branch-tables-x64'
rwx = 'micro-behaviors/mem/alloc/virtual::x64-call-rwx-protect-fourth-arg'

def pe(code, imported='VirtualAlloc'):
    b = bytearray(0xe00)
    def put(off, fmt, *values):
        struct.pack_into('<' + fmt, b, off, *values)
    b[:2] = b'MZ'
    put(0x3c, 'I', 0x80)
    b[0x80:0x84] = b'PE\0\0'
    put(0x84, 'HHIIIHH', 0x8664, 2, 0, 0, 0, 240, 0x22)
    o = 0x98
    put(o, 'H', 0x20b)
    put(o + 4, 'III', 0x600, 0x400, 0)
    put(o + 16, 'IIQ', 0x1000, 0x1000, 0x140000000)
    put(o + 32, 'II', 0x1000, 0x200)
    put(o + 40, 'HHHHHH', 6, 0, 0, 0, 6, 0)
    put(o + 56, 'II', 0x3000, 0x400)
    put(o + 68, 'HH', 3, 0x160)
    put(o + 72, 'QQQQII', 0x100000, 0x1000, 0x100000, 0x1000, 0, 16)
    put(o + 120, 'II', 0x2000, 40)  # Import descriptor directory.
    put(o + 112 + 12 * 8, 'II', 0x2060, 16)
    s = o + 240
    b[s:s+8] = b'.text\0\0\0'
    put(s+8, 'IIIIIIHHI', 0x600, 0x1000, 0x600, 0x400, 0, 0, 0, 0, 0x60000020)
    s += 40
    b[s:s+8] = b'.rdata\0\0'
    put(s+8, 'IIIIIIHHI', 0x400, 0x2000, 0x400, 0xa00, 0, 0, 0, 0, 0x40000040)
    b[0x400:0x400+len(code)] = code
    put(0xa00, 'IIIII', 0x2040, 0, 0, 0x2080, 0x2060)
    put(0xa40, 'Q', 0x20a0)
    put(0xa60, 'Q', 0x20a0)
    b[0xa80:0xa8d] = b'KERNEL32.dll\0'
    name = imported.encode() + b'\0'
    b[0xaa2:0xaa2+len(name)] = name
    return bytes(b)

def call(code):
    # RIP-relative FF15 resolves to the IAT slot at RVA 0x2060.
    return code + b'\xff\x15' + struct.pack('<i', 0x2060-(0x1000+len(code)+6)) + b'\xc3'

# Exact instruction forms observed in the reviewed Rust and flattened images.
indexed = bytes.fromhex('480f48c14889d6488d0d00000000486304814801c8ffe0')
pointer = bytes.fromhex('480f45c14863004801f8ffe0')
setup = bytes.fromhex('31c9ba0010000041b800300000')
mov = bytes.fromhex('41b940000000')
or_flag = bytes.fromhex('4531c94183c940')
register = bytes.fromhex('41b94000000031c9ba0010000041b80030000041ffd04885c0c3')
cases = [
    ('enum-indexed.exe', pe(indexed * 12), [neutral], [flatten, rwx]),
    ('pointer-dispatch.exe', pe(pointer * 12), [neutral, flatten], [rwx]),
    ('eleven-pointer-branches.exe', pe(pointer * 11), [], [neutral, flatten, rwx]),
    ('allocation-import.exe', pe(call(setup + mov)), [rwx], [flatten]),
    ('allocation-or-import.exe', pe(call(setup + or_flag)), [rwx], [flatten]),
    ('heap-import-near-miss.exe', pe(call(setup + mov), 'GetProcessHeap'), [], [rwx, flatten]),
    ('clobbered-argument.exe', pe(call(setup + mov + bytes.fromhex('e800000000'))), [], [rwx]),
    ('resolved-allocation.exe', pe(register), [rwx], [flatten]),
    ('nonexecutable-resolved.exe', pe(register.replace(mov, bytes.fromhex('41b904000000'))), [], [rwx]),
]
with tempfile.TemporaryDirectory(prefix='cmov-allocation-') as directory:
    paths = []
    for name, data, _, _ in cases:
        path = Path(directory) / name
        path.write_bytes(data)
        paths.append(str(path))
    command = [a.atomscan, '--no-update', '--analyze', 'local', '--follow=none', '--format', 'json', *paths]
    result = subprocess.run(command, text=True, capture_output=True)
    if result.returncode:
        raise SystemExit(result.stderr)
    reports = {}
    for line in result.stdout.splitlines():
        for f in json.loads(line)['raw']['files']:
            reports[Path(f['path']).name] = {t['id']: t['crit'] for t in f.get('traits', [])}
    records = []
    for name, _, required, forbidden in cases:
        actual = reports[name]
        assert all(t in actual for t in required), (name, required, actual)
        assert not set(forbidden) & actual.keys(), (name, forbidden, actual)
        if neutral in actual:
            assert actual[neutral] == 3
        if flatten in actual:
            assert actual[flatten] == 4
        if rwx in actual:
            assert actual[rwx] == 3
        records.append({'case': name, 'required': required, 'forbidden': forbidden, 'passed': True})
    Path(a.record).write_text(json.dumps(records, indent=2) + '\n')
    print(f'{len(records)} static PE controls passed')
