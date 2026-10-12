"""Generate inert PE fixtures for triage-sighted controls.

Each image is a minimal valid PE32 whose entry point is a single RET; the
only behavioral content is ASCII strings in the code section, exercising the
string-resolved (*-str / *-text) atoms that fire when the import table hides
an API. No imports, no overlay, no executable payload.
"""
import struct
from pathlib import Path

ROOT = Path(__file__).parent


def image(section_name: bytes, strings: bytes, file_size: int) -> bytes:
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
    data[pos:pos + len(strings)] = strings
    return bytes(data)


SPY_STRINGS = (
    b'GetKeyboardState\x00SetWindowsHookExW\x00CallNextHookEx\x00'
    b'GetClipboardData\x00SetClipboardData\x00EmptyClipboard\x00'
    b'GetProcAddress\x00VirtualAlloc\x00'
)

UPLOAD_STRINGS = (
    b'rifaien yanje v1.0\x00[[UNIQUE]]\x00GetModuleFileNameA\x00'
    b'curl_easy_perform() failed:%s\x00file[]\x00node\x00submit\x00'
    b'http://wecan.hasthe.technology/upload\x00'
)

if __name__ == '__main__':
    (ROOT / 'spy-hidden-imports.exe').write_bytes(
        image(b'.text', SPY_STRINGS, 0x800))
    (ROOT / 'self-upload.exe').write_bytes(
        image(b'UPX1', UPLOAD_STRINGS, 48128))
    (ROOT / 'plain.exe').write_bytes(
        image(b'.text', b'Hello world\x00', 0x800))
