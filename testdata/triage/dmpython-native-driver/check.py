#!/usr/bin/env python3
"""Static native-driver controls: operations versus constants and diagnostics.

Creates inert ELF fixtures; no sample or generated executable is run.
Usage: python3 testdata/triage/dmpython-native-driver/check.py
"""
import json
import os
from pathlib import Path
import struct
import subprocess
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[3]
CLEAVE = os.environ.get("CLEAVE", "cleave")
SOCKET = "micro-behaviors/communications/socket/syscall::x86-64-direct-network-syscalls"
ASSIGN = "micro-behaviors/data/property/assign::auth-token-variable-assignment-source"
PARTITION = "micro-behaviors/fs/disk/partition::partition-table-or-structure-reference"
SIGN = "micro-behaviors/crypto/sign::openssl-rsa-sign-reference"
PAIR = "micro-behaviors/crypto/asymmetric/rsa::rsa-decrypt-sign-reference-pair"
DISK = "micro-behaviors/os/sysinfo/disk::disk-identity-query-reference"
SERIAL = "micro-behaviors/os/sysinfo/disk::id-serial"
WALLET = "micro-behaviors/fs/path/credential::wallet-keystore-file-path-wording"


def elf(path, code, data=b""):
    textoff = 0x100
    rooff = (textoff + len(code) + 15) & ~15
    names = b"\0.text\0.rodata\0.shstrtab\0"
    noff = rooff + len(data)
    shoff = (noff + len(names) + 7) & ~7
    size, base = shoff + 4 * 64, 0x400000
    out = bytearray(size)
    struct.pack_into("<16sHHIQQQIHHHHHH", out, 0,
                     b"\x7fELF\x02\x01\x01" + b"\0" * 9,
                     2, 62, 1, base + textoff, 64, shoff, 0,
                     64, 56, 1, 64, 4, 3)
    struct.pack_into("<IIQQQQQQ", out, 64, 1, 5, 0, base, base, size, size, 0x1000)
    out[textoff:textoff + len(code)] = code
    out[rooff:rooff + len(data)] = data
    out[noff:noff + len(names)] = names
    sections = [(1, 1, 6, base + textoff, textoff, len(code), 16),
                (7, 1, 2, base + rooff, rooff, len(data), 1),
                (15, 3, 0, 0, noff, len(names), 1)]
    for i, (name, kind, flags, addr, off, length, align) in enumerate(sections, 1):
        struct.pack_into("<IIQQQQIIQQ", out, shoff + i * 64,
                         name, kind, flags, addr, off, length, 0, 0, align, 0)
    path.write_bytes(out)


def reports(text):
    decoder = json.JSONDecoder()
    while text.strip():
        obj, end = decoder.raw_decode(text.lstrip())
        text = text.lstrip()[end:]
        yield obj


with tempfile.TemporaryDirectory(prefix="dmpython-controls-") as tmp:
    dest = Path(tmp)
    elf(dest / "syscall-pair.elf", bytes.fromhex(
        "b8 29 00 00 00 0f 05 b8 2a 00 00 00 0f 05 c3"))
    elf(dest / "constants.elf", bytes.fromhex(
        "b8 29 00 00 00 c3 b8 2a 00 00 00 c3 bf 29 00 00 00 c3"))
    elf(dest / "unrelated-syscall.elf", bytes.fromhex(
        "bf 29 00 00 00 b8 01 00 00 00 0f 05 c3"))
    elf(dest / "sql-template.elf", b"\xc3",
        b"partition information of the partition table\0"
        b"AUTH_ENCRYPT_NAME = %-10s #User password encrypt name\0named\0mysql compatible mode\0")
    elf(dest / "disk-structure.elf", b"\xc3", b"PARTITION_INFORMATION_EX\0")
    elf(dest / "rsa.elf", b"\xc3", b"RSA_sign\0RSA_public_decrypt\0")
    elf(dest / "udev-label.elf", b"\xc3", b"ID_SERIAL\0")
    elf(dest / "udev-query.elf", b"\xc3", b"udevadm info --query=property --name /dev/%s | grep '^ID_SERIAL='\0")
    elf(dest / "wallet.elf", b"\xc3", b"no legal wallet file in that path\0")
    (dest / "assignment.js").write_text('const AUTH_TOKEN = "session-token";\n')
    (dest / "author.js").write_text('const AUTHOR = "Ada";\n')
    (dest / "query.sh").write_text("#!/bin/sh\nlsblk -o NAME,SERIAL\n")
    # Deliberately unrelated members: a small extension, a large vendored
    # library, and metadata without Author/Requires-Dist are normal packaging.
    with zipfile.ZipFile(dest / "driver-1.0-cp310-cp310-linux_x86_64.whl",
                         "w", compression=zipfile.ZIP_DEFLATED) as wheel:
        wheel.writestr("driver.cpython-310-x86_64-linux-gnu.so", (dest / "constants.elf").read_bytes())
        wheel.writestr("driver.libs/libclient.so", (dest / "constants.elf").read_bytes() + b"\0" * 16000000)
        wheel.writestr("driver-1.0.dist-info/METADATA", "Metadata-Version: 2.1\nName: driver\nVersion: 1.0\n\n")
        wheel.writestr("driver-1.0.dist-info/WHEEL", "Wheel-Version: 1.0\nRoot-Is-Purelib: false\nTag: cp310-cp310-linux_x86_64\n")
    run = subprocess.run([CLEAVE, "--traits-dir", str(ROOT), "--format", "json", str(dest)],
                         text=True, capture_output=True)
    if run.returncode:
        raise SystemExit(run.stderr + run.stdout[-2000:])
    by_name = {}
    for report in reports(run.stdout):
        for file in report["files"]:
            if "!!" not in file["path"]:
                by_name[Path(file["path"]).name] = {t["id"] for t in file["traits"]}
    cases = {
        "syscall-pair.elf": ({SOCKET}, set()),
        "constants.elf": (set(), {SOCKET}),
        "unrelated-syscall.elf": (set(), {SOCKET}),
        "sql-template.elf": (set(), {PARTITION, ASSIGN, SOCKET}),
        "disk-structure.elf": ({PARTITION}, set()),
        "rsa.elf": ({SIGN, PAIR}, set()),
        "udev-label.elf": ({SERIAL}, {DISK}),
        "udev-query.elf": ({"micro-behaviors/os/sysinfo/disk::udevadm-disk-property-query-command"}, set()),
        "wallet.elf": ({WALLET}, set()),
        "assignment.js": ({ASSIGN}, set()),
        "author.js": (set(), {ASSIGN}),
        "query.sh": ({"micro-behaviors/os/sysinfo/disk::lsblk-name-serial-command"}, set()),
        "driver-1.0-cp310-cp310-linux_x86_64.whl": (
            {"metadata/file/archive::member-at-least-10mb"},
            {"objectives/supply-chain/hidden-payload/native-extension::pypi-massive-native-extension-minimal-metadata"}),
    }
    for name, (required, forbidden) in cases.items():
        actual = by_name[name]
        assert required <= actual, (name, "missing", required - actual)
        assert not forbidden & actual, (name, "unexpected", forbidden & actual)
    print(f"PASS: {len(cases)} native-driver controls")
