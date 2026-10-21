#!/usr/bin/env python3
"""Check resource-code placement and BIOS read/transfer boundaries."""
import argparse
import json
import struct
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TRAIT = 'metadata/binary/resource/boot-loader::bios-read-far-transfer'


def pe_fixture(code, section=b'.rsrc'):
    """An inert PE carrying code bytes; no resource activation is implied."""
    b = bytearray(0x800)
    b[:2] = b'MZ'
    struct.pack_into('<I', b, 0x3c, 0x80)
    b[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', b, 0x84, 0x14c, 2, 0, 0, 0, 224, 0x102)
    o = 0x98
    struct.pack_into('<H', b, o, 0x10b)
    struct.pack_into('<III', b, o + 16, 0x1000, 0x1000, 0x2000)
    struct.pack_into('<III', b, o + 28, 0x400000, 0x1000, 0x200)
    struct.pack_into('<II', b, o + 56, 0x3000, 0x400)
    struct.pack_into('<H', b, o + 68, 3)
    struct.pack_into('<I', b, o + 92, 16)
    for n, (name, rva, raw, flags) in enumerate([
            (b'.text', 0x1000, 0x400, 0x60000020),
            (section, 0x2000, 0x600, 0x40000040)]):
        sh = o + 224 + 40*n
        b[sh:sh+8] = name.ljust(8, b'\0')
        struct.pack_into('<IIII', b, sh+8, 0x200, rva, 0x200, raw)
        struct.pack_into('<I', b, sh+36, flags)
    b[0x400] = 0xc3
    b[0x620:0x620+len(code)] = code
    return bytes(b)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--scratch', type=Path, required=True)
    ap.add_argument('--cleave', default='cleave')
    a = ap.parse_args()
    a.scratch.mkdir(parents=True, exist_ok=True)
    code = bytes.fromhex('b80102b500b600b129b280cd13720868c0076a009090cb')
    varied = bytes.fromhex('b80102b501b602b103b281cd1372146800906a00cb')
    cases = [
        ('resource-code.exe', pe_fixture(code), True),
        ('other-disk-sector-segment.exe', pe_fixture(varied), True),
        ('video-interrupt.exe', pe_fixture(code.replace(b'\xcd\x13', b'\xcd\x10')), False),
        ('disk-write.exe', pe_fixture(code.replace(b'\xb8\x01\x02', b'\xb8\x01\x03')), False),
        ('no-far-transfer.exe', pe_fixture(code[:-1]+b'\xc3'), False),
        ('no-bios-call.exe', pe_fixture(code.replace(b'\xcd\x13', b'\x90\x90')), False),
        ('ordinary-data.exe', pe_fixture(b'An ordinary resource string\0'), False),
        ('other-section.exe', pe_fixture(code, b'.data'), False),
    ]
    for name, data, _ in cases:
        (a.scratch / name).write_bytes(data)
    cmd = [a.cleave, '--traits-dir', str(ROOT), '--no-update-check',
           '--disable', 'third-party,radare2,upx', '--format', 'json']
    cmd += [str(a.scratch / name) for name, _, _ in cases]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    decoder = json.JSONDecoder()
    stream = result.stdout.lstrip()
    files = []
    while stream:
        record, end = decoder.raw_decode(stream)
        files.extend(record['files'])
        stream = stream[end:].lstrip()
    for name, _, expected in cases:
        f = next(f for f in files if f['path'] == str(a.scratch / name))
        matches = [t for t in f.get('traits', []) if t['id'] == TRAIT]
        assert bool(matches) == expected, (name, matches, expected)
        assert all(t['crit'] == 3 for t in matches), (name, matches)
    print(f'{len(cases)} resource-code controls passed')


if __name__ == '__main__':
    main()
