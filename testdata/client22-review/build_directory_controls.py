"""Build inert PE controls for directory-result concealment. Never executes PE code.

RET is the entry point; unreachable analysis fragments follow it. The positive
combines result removal and hook support. Near misses separate local filtering
from a DLL that merely references directory and code-patching APIs.
"""
from pathlib import Path
import struct

TESTDATA = Path(__file__).resolve().parents[1]
GATE = bytes.fromhex(
    'ff 15 00 00 00 00 44 8b e0 85 c0 0f 88 00 00 00 00 '
    '83 fb 26 0f 87 00 00 00 00 48 b8 0e 10 00 00 60 00 00 00 '
    '48 0f a3 d8 0f 83 00 00 00 00')
COMPACT = bytes.fromhex(
    '8b 17 8b c2 85 d2 0f 84 00 00 00 00 48 63 c6 44 8b cf 45 2b cf '
    '0f b6 84 03 00 00 00 00 8b 8c 83 00 00 00 00 48 03 cb ff e1 '
    '8b c2 eb 02 33 c0 45 8b c5 44 2b c0 48 63 c6 45 2b c1 '
    '0f b6 84 03 00 00 00 00 8b 8c 83 00 00 00 00 48 03 cb ff e1 '
    '33 d2 48 03 d7 48 8b cf e8 00 00 00 00')


def pe(code, imports):
    data = bytearray(0x1400)
    data[:2] = b'MZ'
    struct.pack_into('<I', data, 0x3c, 0x80)
    data[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', data, 0x84, 0x8664, 2, 0, 0, 0, 240, 0x22)
    opt = 0x98
    struct.pack_into('<H', data, opt, 0x20b)
    struct.pack_into('<III', data, opt + 4, 0x200, 0x1000, 0)
    struct.pack_into('<II', data, opt + 16, 0x1000, 0x1000)
    struct.pack_into('<Q', data, opt + 24, 0x140000000)
    struct.pack_into('<II', data, opt + 32, 0x1000, 0x200)
    struct.pack_into('<HH', data, opt + 40, 6, 0)
    struct.pack_into('<III', data, opt + 52, 0, 0x3000, 0x200)
    struct.pack_into('<H', data, opt + 68, 3)
    struct.pack_into('<I', data, opt + 108, 16)
    for i, (name, rva, offset, size, flags) in enumerate([
        (b'.text', 0x1000, 0x200, 0x200, 0x60000020),
        (b'.rdata', 0x2000, 0x400, 0x1000, 0x40000040),
    ]):
        pos = opt + 240 + 40 * i
        data[pos:pos + 8] = name.ljust(8, b'\0')
        struct.pack_into('<IIIIIIHHI', data, pos + 8,
                         size, rva, size, offset, 0, 0, 0, 0, flags)
    data[0x200] = 0xc3
    assert len(code) <= 0x1e0
    data[0x220:0x220 + len(code)] = code
    cur = 0x400 + 20 * (len(imports) + 1)
    for i, name in enumerate(imports):
        thunk = cur
        cur += 16
        hint = cur
        blob = b'\0\0' + name.encode() + b'\0'
        data[cur:cur + len(blob)] = blob
        cur = (cur + len(blob) + 1) & ~1
        dll = cur
        data[cur:cur + 13] = b'kernel32.dll\0'
        cur += 13
        struct.pack_into('<Q', data, thunk, hint - 0x400 + 0x2000)
        struct.pack_into('<IIIII', data, 0x400 + i * 20,
                         thunk - 0x400 + 0x2000, 0, 0,
                         dll - 0x400 + 0x2000, thunk - 0x400 + 0x2000)
    if imports:
        struct.pack_into('<II', data, opt + 120, 0x2000, 20 * (len(imports) + 1))
    name = b'ZwQueryDirectoryFile\0'
    data[cur:cur + len(name)] = name
    assert cur + len(name) <= len(data)
    return data


if __name__ == '__main__':
    code = GATE + b'\x90' * 96 + COMPACT
    hooks = ['GetProcAddress', 'VirtualProtect', 'FlushInstructionCache']
    cases = [
        ('hostile/native-directory-result-hide-hook.exe', code, hooks),
        ('benign/native-directory-query-hooks-only.exe', b'\xc3', hooks),
        ('benign/native-directory-result-filter-only.exe', code, []),
    ]
    for path, fragment, imports in cases:
        (TESTDATA / path).write_bytes(pe(fragment, imports))
