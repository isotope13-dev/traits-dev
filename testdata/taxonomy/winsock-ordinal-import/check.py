"""Check DLL-bound Winsock ordinal imports in inert PE32/PE32+ images.

The entry point is RET. Import tables describe capabilities, not executed calls.
The original PrintDemon DLL supplies the separate real-world positive case.
"""
import argparse
import json
import os
from pathlib import Path
import struct
import subprocess

ROOT = Path(__file__).resolve().parents[3]
BIND = "micro-behaviors/communications/socket/bind/function::winsock-bind-ordinal-import"
LISTEN = "micro-behaviors/communications/socket/listen::winsock-listen-ordinal-import"
TARGETS = {BIND, LISTEN}


def image(library, imports, bits):
    data = bytearray(0xa00)
    data[:2] = b"MZ"
    struct.pack_into("<I", data, 0x3c, 0x80)
    data[0x80:0x84] = b"PE\0\0"
    optional_size = 240 if bits == 64 else 224
    struct.pack_into("<HHIIIHH", data, 0x84,
                     0x8664 if bits == 64 else 0x14c,
                     2, 0, 0, 0, optional_size, 0x22 if bits == 64 else 0x102)
    opt = 0x98
    struct.pack_into("<H", data, opt, 0x20b if bits == 64 else 0x10b)
    for off, value in {4: 0x200, 8: 0x600, 16: 0x1000, 20: 0x1000,
                       32: 0x1000, 36: 0x200, 56: 0x3000, 60: 0x200}.items():
        struct.pack_into("<I", data, opt + off, value)
    struct.pack_into("<H", data, opt + 68, 3)
    if bits == 64:
        struct.pack_into("<Q", data, opt + 24, 0x140000000)
        directories = opt + 112
    else:
        struct.pack_into("<II", data, opt + 24, 0x2000, 0x400000)
        directories = opt + 96
    struct.pack_into("<I", data, directories - 4, 16)
    struct.pack_into("<II", data, directories + 8, 0x2000, 40)
    for index, (name, rva, raw, size, flags) in enumerate([
        (b".text", 0x1000, 0x200, 0x200, 0x60000020),
        (b".rdata", 0x2000, 0x400, 0x600, 0x40000040),
    ]):
        struct.pack_into("<8sIIIIIIHHI", data, opt + optional_size + index * 40,
                         name, size, rva, size, raw, 0, 0, 0, 0, flags)
    data[0x200] = 0xc3
    struct.pack_into("<IIIII", data, 0x400, 0x2100, 0, 0, 0x2080, 0x2180)
    dll = library.encode() + b"\0"
    data[0x480:0x480 + len(dll)] = dll
    # A decoy Winsock string must not attach another DLL's ordinals to Winsock.
    data[0x4c0:0x4cb] = b"WS2_32.dll\0"
    cursor = 0x600
    width = bits // 8
    for index, item in enumerate(imports):
        if isinstance(item, int):
            thunk = (1 << (bits - 1)) | item
        else:
            encoded = b"\0\0" + item.encode() + b"\0"
            data[cursor:cursor + len(encoded)] = encoded
            thunk = cursor + 0x1c00
            cursor += len(encoded) + len(encoded) % 2
        for raw in [0x500, 0x580]:
            struct.pack_into("<Q" if bits == 64 else "<I",
                             data, raw + width * index, thunk)
    return data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    cases = [
        ("both", "WS2_32.dll", [2, 13], TARGETS),
        ("legacy", "WSOCK32.dll", [2, 13], TARGETS),
        ("mixed-case", "wS2_32.DlL", [2, 13], TARGETS),
        ("bind-only", "WS2_32.dll", [2], {BIND}),
        ("listen-only", "WS2_32.dll", [13], {LISTEN}),
        ("different-dll", "ordinary.dll", [2, 13], set()),
        ("other-ordinals", "WS2_32.dll", [4, 23], set()),
        ("named-imports", "WS2_32.dll", ["bind", "listen"], set()),
    ]
    for bits in [32, 64]:
        for name, library, imports, expected in cases:
            path = args.output / f"{name}-{bits}.exe"
            path.write_bytes(image(library, imports, bits))
            result = subprocess.run([
                os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
                "--disable", "radare2,upx", "--format", "json", str(path),
            ], capture_output=True, text=True, check=True, cwd=ROOT)
            report = json.loads(result.stdout)
            actual = {t["id"] for f in report["files"]
                      for t in f.get("traits", [])} & TARGETS
            assert actual == expected, (path.name, expected, actual)
            print(f"{path.name}: PASS", flush=True)


if __name__ == "__main__":
    main()
