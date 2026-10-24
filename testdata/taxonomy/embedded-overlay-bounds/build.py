"""Build inert PE32/PE32+ controls for appended section-bound checks."""
from pathlib import Path
import struct

ROOT = Path(__file__).parent

def image(bits=32, payload=b"\xc3"):
    data = bytearray(1024)
    data[:16] = bytes.fromhex("4d5a90000300000004000000ffff0000")
    struct.pack_into("<I", data, 60, 128)
    data[128:132] = b"PE\0\0"
    optsize = 224 if bits == 32 else 240
    struct.pack_into("<HHIIIHH", data, 132, 0x14c if bits == 32 else 0x8664,
                     1, 0, 0, 0, optsize, 0x102 if bits == 32 else 0x22)
    at = 152
    struct.pack_into("<H", data, at, 0x10b if bits == 32 else 0x20b)
    struct.pack_into("<III", data, at+4, 512, 0, 0)
    struct.pack_into("<II", data, at+16, 4096, 4096)
    if bits == 32:
        struct.pack_into("<II", data, at+24, 8192, 0x400000)
        struct.pack_into("<I", data, at+92, 16)
    else:
        struct.pack_into("<Q", data, at+24, 0x140000000)
        struct.pack_into("<I", data, at+108, 16)
    struct.pack_into("<II", data, at+32, 4096, 512)
    struct.pack_into("<HH", data, at+40, 6, 0)
    struct.pack_into("<II", data, at+56, 8192, 512)
    struct.pack_into("<H", data, at+68, 3)
    section = at+optsize
    data[section:section+8] = b".text\0\0\0"
    struct.pack_into("<IIII", data, section+8, 512, 4096, 512, 512)
    struct.pack_into("<I", data, section+36, 0x60000020)
    data[512:512+len(payload)] = payload
    return bytes(data)

outer = image()
for bits in (32, 64):
    inner = image(bits)
    (ROOT / f"complete-{bits}.exe").write_bytes(outer+inner)
    (ROOT / f"truncated-{bits}.exe").write_bytes(outer+inner[:-1])
(ROOT / "no-overlay.exe").write_bytes(outer)
bad = bytearray(image()); bad[128] = 0
(ROOT / "bad-signature.exe").write_bytes(outer+bad[:-1])
(ROOT / "header-only.exe").write_bytes(outer+image()[:64])
# A valid header-looking sequence in mapped code is not an overlay finding.
(ROOT / "mapped-header.exe").write_bytes(image(payload=image()[:511]))
