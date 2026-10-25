"""Static controls, not executable reconstructions of the malware.

Instruction relationships come from the reviewed x64 startup stub. Immediate
keys and branch distances are varied; neither names nor exact sizes convict.
"""
from pathlib import Path
import struct

ROOT = Path(__file__).parent

def pe(text, names):
    data = bytearray(1536)
    data[:2] = b'MZ'
    struct.pack_into('<I', data, 60, 128)
    data[128:132] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', data, 132, 0x8664, 2, 0, 0, 0, 240, 0x22)
    o = 152
    struct.pack_into('<H', data, o, 0x20b)
    struct.pack_into('<I', data, o+16, 0x1000)
    struct.pack_into('<Q', data, o+24, 0x140000000)
    struct.pack_into('<II', data, o+32, 0x1000, 512)
    struct.pack_into('<II', data, o+56, 0x3000, 512)
    struct.pack_into('<H', data, o+68, 3)
    struct.pack_into('<I', data, o+108, 16)
    struct.pack_into('<II', data, o+120, 0x2000, 40)
    for j, (name, rva, off, flags) in enumerate([
        (b'.text', 0x1000, 512, 0x60000020),
        (b'.rdata', 0x2000, 1024, 0x40000040),
    ]):
        at = 392+j*40
        data[at:at+8] = name.ljust(8, b'\0')
        struct.pack_into('<IIII', data, at+8, 512, rva, 512, off)
        struct.pack_into('<I', data, at+36, flags)
    data[512:512+len(text)] = text
    struct.pack_into('<IIIII', data, 1024, 0x2040, 0, 0, 0x20c0, 0x2080)
    data[1216:1229] = b'KERNEL32.dll\0'
    at = 0x2100
    for j, name in enumerate(names):
        struct.pack_into('<Q', data, 1024+0x40+j*8, at)
        struct.pack_into('<Q', data, 1024+0x80+j*8, at)
        raw = b'\0\0'+name.encode()+b'\0'
        off = 1024+at-0x2000
        data[off:off+len(raw)] = raw
        at += len(raw)
    return data

# Keys and branch offsets deliberately differ from the specimen.
decoder = bytes.fromhex(
    '66 45 81 03 17 42 E9 02 00 00 00 CC CC '
    '41 81 2B 21 43 65 87 E9 03 00 00 00 CC CC CC '
    '4D 83 C3 02 E9 01 00 00 00 CC '
    '4A 81 FF 00 10 00 00 E9 02 00 00 00 CC CC')
handoff = bytes.fromhex(
    '49 81 EB 00 10 00 00 49 8B FB 48 89 F9 '
    '48 BA 00 10 00 00 00 00 00 00 '
    '4D B8 20 00 00 00 00 00 00 00 4B 89 E1 '
    '42 FF 15 12 34 00 00 48 8B CF '
    '48 81 C7 00 08 00 00 48 FF D7 48 89 EC C3')
for name, code, imports in [
    ('decoder-handoff.exe', decoder+handoff, ['VirtualProtect']),
    ('decoder-only.exe', decoder+b'\xc3', ['VirtualProtect']),
    ('handoff-only.exe', handoff, ['VirtualProtect']),
    ('api-profile-only.exe', b'\xc3', ['CreateFiber', 'NtCreateSection', 'NtMapViewOfSection', 'VirtualProtect', 'LoadLibraryA', 'GetProcAddress']),
]:
    (ROOT/name).write_bytes(pe(code, imports))
