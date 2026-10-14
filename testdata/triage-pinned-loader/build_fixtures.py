"""Generate inert PE fixtures for triage-pinned-loader controls.

xor-loop.exe is a minimal valid PE32 whose only behavioral content is one
counted `xorb imm8, disp(%rbp,%rax)` stack-decode loop in .text -- the shape
matched by micro-behaviors/crypto/symmetric/xor/loop::x64-rbp-xor-imm8-counted-loop.
No imports, no exports, no overlay, no executable payload.
"""
import struct
from pathlib import Path

ROOT = Path(__file__).parent


def image(section_name: bytes, code: bytes, file_size: int) -> bytes:
    data = bytearray(max(0x800, file_size))
    data[:2] = b'MZ'
    struct.pack_into('<I', data, 0x3c, 0x80)
    data[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', data, 0x84, 0x14c, 1, 1700000000, 0, 0, 224, 0x102)
    opt = 0x98
    struct.pack_into('<H', data, opt, 0x10b)
    data[opt + 2] = 14
    for off, val in {4: 512, 8: 4096, 16: 0x1000, 20: 0x1000, 24: 0x2000,
                     28: 0x400000, 32: 0x1000, 36: 0x200, 56: 0x5000,
                     60: 0x200, 72: 0x100000, 76: 0x1000, 80: 0x100000,
                     84: 0x1000, 92: 16}.items():
        struct.pack_into('<I', data, opt + off, val)
    struct.pack_into('<HH', data, opt + 40, 6, 0)
    struct.pack_into('<HH', data, opt + 48, 6, 0)
    struct.pack_into('<H', data, opt + 68, 3)
    sec = opt + 224
    raw_size = len(data) - 0x200
    struct.pack_into('<8sIIIIIIHHI', data, sec, section_name, raw_size,
                     0x1000, raw_size, 0x200, 0, 0, 0, 0, 0x60000020)
    data[0x200] = 0xc3
    pos = 0x201
    data[pos:pos + len(code)] = code
    return bytes(data)


# xorb $0x37, -0x41(%rbp,%rax); inc %rax; cmp $0x0c, %rax; jb -14
XOR_LOOP = bytes.fromhex('80 74 05 bf 37 48 ff c0 48 83 f8 0c 72 f2')

if __name__ == '__main__':
    (ROOT / 'xor-loop.exe').write_bytes(image(b'.text', XOR_LOOP, 0x800))
