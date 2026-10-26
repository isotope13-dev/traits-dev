#!/usr/bin/env python3
"""Generate inert byte fixtures to test native decoder relationships."""
import json
import os
from pathlib import Path
import struct
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CLEAVE = os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave'))
NATIVE = 'objectives/anti-static/obfuscation/encoding/arithmetic::x86-unrolled-ecx-decoded-range-call'
DOS = 'objectives/anti-static/obfuscation/payload/polymorphic/decryptor::dos-junked-incrementing-word-decoder'
PREFETCH = 'objectives/anti-analysis/emulator-detect::dos-prefetched-nop-jump-patch'


def u16(b, off, value):
    struct.pack_into('<H', b, off, value & 65535)


def u32(b, off, value):
    struct.pack_into('<I', b, off, value & 0xffffffff)


def native():
    b = bytearray(0x1400)
    b[:2] = b'MZ'
    u32(b, 0x3c, 0x80)
    b[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', b, 0x84, 0x14c, 1, 0, 0, 0, 0xe0, 0x102)
    op = 0x98
    u16(b, op, 0x10b)
    u32(b, op+16, 0x1000)
    u32(b, op+20, 0x1000)
    u32(b, op+28, 0x400000)
    u32(b, op+32, 0x1000)
    u32(b, op+36, 0x200)
    u32(b, op+56, 0x3000)
    u32(b, op+60, 0x200)
    u16(b, op+68, 3)
    u32(b, op+92, 16)
    sh = op+0xe0
    b[sh:sh+8] = b'.code\0\0\0'
    struct.pack_into('<IIII', b, sh+8, 0x1200, 0x1000, 0x1200, 0x200)
    u32(b, sh+36, 0xe0000020)
    b[0x200] = 0xc3  # Entry returns; snippets are never invoked.
    head, decoded = 0x800, 0x300
    prefix = bytes.fromhex('50515253555657e8000000005981e9')
    h = prefix+struct.pack('<I', head+12-decoded)+bytes.fromhex('ba0000000051')
    operations = bytes.fromhex('81813c0000007856341281b18000000021436587')
    tail = head+len(h)+len(operations)
    t = bytearray(bytes.fromhex('81c24000000081c14000000081fa000100007405e900000000e8000000005f5e5d5b5a5958'))
    u32(t, 21, head+25-(tail+25))
    u32(t, 26, decoded+0x20-(tail+30))
    b[head:head+len(h)] = h
    b[head+len(h):tail] = operations
    b[tail:tail+len(t)] = t
    return b, head, tail, sh


def dos():
    b = bytearray(0x500)
    b[0] = 0xe9
    entry = 0x300
    u16(b, 1, entry-3)
    b[3:6] = bytes.fromhex('b44ccd')
    b[entry:entry+12] = bytes.fromhex('b83412be3322d1c646bb0002')
    count, xor, advance, patch = entry+50, entry+90, entry+130, entry+20
    b[count:count+14] = bytes.fromhex('8b3e1111ba800181c6222246d1c6')
    b[xor:xor+7] = bytes.fromhex('2e310743434a4a')
    b[advance:advance+13] = bytes.fromhex('81c04fa04146fc9d7403e90000')
    u16(b, advance+11, xor-(advance+13))
    b[patch:patch+9] = bytes.fromhex('2ec7060000ebc09090')
    u16(b, patch+3, patch+7+0x100)
    return b, entry, count, xor, advance, patch


def main():
    cases = []

    def add(name, b, required=(), forbidden=()):
        cases.append((name, bytes(b), set(required), set(forbidden)))

    b, head, tail, sh = native()
    add('native-original.exe', b, [NATIVE])
    for name, off, value in [
        ('changed-key', head+25+6, 0x87654321),
        ('changed-stride', tail+2, 0x80),
        ('bad-back-edge', tail+21, 0),
        ('bad-call', tail+26, 0),
        ('odd-size', tail+14, 0x101),
    ]:
        v = bytearray(b)
        u32(v, off, value)
        add('native-'+name+'.exe', v, [NATIVE] if name == 'changed-key' else (),
            () if name == 'changed-key' else [NATIVE])
    v = bytearray(b)
    v[sh:sh+8] = b'PAYLOAD\0'
    add('native-section-renamed.exe', v, [NATIVE])
    v = bytearray(b)
    u32(v, sh+36, 0xc0000040)
    add('native-non-executable.exe', v, (), [NATIVE])
    b, entry, count, xor, advance, patch = dos()
    add('dos-original.com', b, [DOS, PREFETCH])
    for name, off, value, required, forbidden in [
        ('changed-key', entry+1, 0x7194, [DOS, PREFETCH], []),
        ('wrong-entry', 1, entry-2, [PREFETCH], [DOS]),
        ('wrong-back-edge', advance+11, 0, [PREFETCH], [DOS]),
        ('odd-count', count+5, 0x181, [PREFETCH], [DOS]),
        ('patch-elsewhere', patch+3, 0x1234, [DOS], [PREFETCH]),
    ]:
        v = bytearray(b)
        u16(v, off, value)
        add('dos-'+name+'.com', v, required, forbidden)
    v = bytearray(b)
    v[patch+6] = 16
    add('dos-forward-patch.com', v, [DOS], [PREFETCH])
    with tempfile.TemporaryDirectory(prefix='decoder-byte-controls-') as temporary:
        paths = []
        for name, data, _, _ in cases:
            p = Path(temporary)/name
            p.write_bytes(data)
            paths.append(str(p))
        run = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), '--format', 'jsonl', *paths],
                             text=True, capture_output=True, check=True)
        remaining = run.stdout.lstrip()
        decoder = json.JSONDecoder()
        findings = {}
        while remaining:
            d, end = decoder.raw_decode(remaining)
            remaining = remaining[end:].lstrip()
            for f in d.get('files', []):
                findings[Path(f['path']).name] = {t['id'] for t in f.get('traits', [])}
        for name, _, required, forbidden in cases:
            ids = findings[name]
            assert required <= ids, (name, 'missing', sorted(required-ids))
            assert not forbidden & ids, (name, 'unexpected', sorted(forbidden & ids))
    print(json.dumps({'passed': len(cases), 'cases': [c[0] for c in cases]}, indent=2))


if __name__ == '__main__':
    main()
