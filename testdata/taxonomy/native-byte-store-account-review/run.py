#!/usr/bin/env python3
"""Check instruction-only classification and import-versus-text boundaries."""
import pathlib
import re
import struct
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[3]
STORE = "metadata/binary/instruction::x86-stack-immediate-byte-run"
DELETE = "micro-behaviors/os/user/delete::net-user-del-import"


def image(code=b"\xc3", data=b"", imported=None):
    buf = bytearray(1536)
    buf[:2] = b"MZ"
    struct.pack_into("<I", buf, 0x3c, 0x80)
    buf[0x80:0x84] = b"PE\0\0"
    struct.pack_into("<HHIIIHH", buf, 0x84, 0x14c, 2, 0, 0, 0, 224, 0x102)
    opt = 0x98
    struct.pack_into("<H", buf, opt, 0x10b)
    struct.pack_into("<III", buf, opt + 16, 0x1000, 0x1000, 0x2000)
    struct.pack_into("<III", buf, opt + 28, 0x400000, 4096, 512)
    struct.pack_into("<II", buf, opt + 56, 0x3000, 512)
    struct.pack_into("<H", buf, opt + 68, 3)
    struct.pack_into("<I", buf, opt + 92, 16)
    for k, (name, va, off, flags) in enumerate([
        (b".text", 0x1000, 512, 0x60000020),
        (b".rdata", 0x2000, 1024, 0x40000040),
    ]):
        struct.pack_into("<8sIIIIIIHHI", buf, opt + 224 + k * 40,
                         name, 512, va, 512, off, 0, 0, 0, 0, flags)
    buf[512:512 + len(code)] = code
    buf[1280:1280 + len(data)] = data
    if imported:
        struct.pack_into("<II", buf, opt + 104, 0x2000, 40)
        struct.pack_into("<IIIII", buf, 1024, 0x2040, 0, 0, 0x2060, 0x2050)
        struct.pack_into("<I", buf, 1088, 0x2080)
        struct.pack_into("<I", buf, 1104, 0x2080)
        buf[1120:1133] = b"NETAPI32.dll\0"
        name = b"\0\0" + imported.encode() + b"\0"
        buf[1152:1152 + len(name)] = name
    return buf


# These stores construct ordinary text; their bytes do not establish shellcode.
stores = b"".join(bytes([0xc6, 0x45, 0x80 + i, c])
                  for i, c in enumerate(b"REG_MULTI_SZ"))
cases = [
    ("ordinary-stack-label", image(stores + b"\xc3"), {STORE}),
    ("eleven-stores", image(stores[:-4] + b"\xc3"), set()),
    ("stores-in-data", image(data=stores), set()),
    ("account-delete-import", image(imported="NetUserDel"), {DELETE}),
    ("other-account-import", image(imported="NetUserGet"), set()),
    ("account-delete-text-only", image(data=b"NetUserDel\0"), set()),
    ("both-observations", image(stores, imported="NetUserDel"), {STORE, DELETE}),
]
engine = sys.argv[1] if len(sys.argv) > 1 else "cleave"
with tempfile.TemporaryDirectory(prefix="native-trait-review-") as temp:
    for name, buf, expected in cases:
        path = pathlib.Path(temp, name + ".exe")
        path.write_bytes(buf)
        result = subprocess.run(
            [engine, "--traits-dir", str(ROOT), "--disable", "yara,radare2,upx",
             "test-rules", str(path), "--rules", ",".join([STORE, DELETE])],
            capture_output=True, text=True, cwd=ROOT)
        output = result.stdout + result.stderr
        actual = {rule for rule in [STORE, DELETE]
                  if re.search(r"^MATCHED " + re.escape(rule) + r" \(trait\)", output, re.M)}
        if result.returncode or actual != expected:
            raise SystemExit(f"{name}: expected {expected}, got {actual}\n{output}")
        print(name + ": passed")

