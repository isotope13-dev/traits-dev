#!/usr/bin/env python3
"""Persisted .NET polling-keylogger exfiltration composite.

Builds minimal non-executable PE32 fixtures (named sections, no entry
point, no imports) and checks the hostile composite covering a managed
stub that polls GetAsyncKeyState, writes a CurrentVersion Run key, and
moves data over TcpClient: all three legs must hold, and dropping the
network leg must silence it, as must a plain assembly with none of the
behavior legs.
"""
from __future__ import annotations

import argparse
import json
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

PERSISTED = ("objectives/collection/keylog/polling::"
             "dotnet-persisted-polling-keylog-exfil")

RUN_KEY = b"Software\\Microsoft\\Windows\\CurrentVersion\\Run\0"
KEYLOG = b"GetAsyncKeyState\0"
NETWORK = b"TcpClient\0NetworkStream\0"
ASSEMBLY = b"mscorlib, Version=4.0.0.0\0"


def pe32(text: bytes, rdata: bytes) -> bytes:
    """Minimal PE32: DOS stub, two sections, no imports, no entry point."""
    file_align = 0x200
    text_raw = 0x200
    rdata_raw = (len(rdata) + file_align - 1) & ~(file_align - 1)
    headers_len = 64 + 4 + 20 + 224 + 2 * 40
    size_headers = (headers_len + file_align - 1) & ~(file_align - 1)
    total = size_headers + file_align + rdata_raw
    data = bytearray(total)
    data[0:2] = b"MZ"
    struct.pack_into("<I", data, 0x3C, 64)
    data[64:68] = b"PE\0\0"
    struct.pack_into("<HHIIIHH", data, 68, 0x14C, 2, 0, 0, 0, 224, 0x010F)
    opt = 68 + 20
    struct.pack_into("<H", data, opt, 0x10B)
    struct.pack_into("<III", data, opt + 16, 0x1000, 0x1000, 0x2000)
    struct.pack_into("<I", data, opt + 28, 0x400000)
    struct.pack_into("<II", data, opt + 32, 0x1000, 0x200)
    struct.pack_into("<II", data, opt + 56, 0x3000, size_headers)
    struct.pack_into("<H", data, opt + 68, 3)
    struct.pack_into("<I", data, opt + 92, 16)
    sect = opt + 224
    struct.pack_into("<8sIIIIIIHHI", data, sect, b".text\0\0\0",
                     len(text), 0x1000, file_align, text_raw, 0, 0, 0, 0,
                     0x60000020)
    struct.pack_into("<8sIIIIIIHHI", data, sect + 40, b".rdata\0\0",
                     len(rdata), 0x2000, rdata_raw,
                     size_headers + file_align, 0, 0, 0, 0, 0x40000040)
    data[text_raw:text_raw + len(text)] = text
    off = size_headers + file_align
    data[off:off + len(rdata)] = rdata
    return bytes(data)


FIXTURES = {
    # Assembly marker, keylog polling, Run key, TCP channel: fires.
    "persisted-keylog-exfil.exe": (
        b"BSJB\x00\xc3",
        ASSEMBLY + KEYLOG + RUN_KEY + NETWORK,
        {PERSISTED},
        set(),
    ),
    # Same but no network channel: must stay silent.
    "keylog-run-no-network.exe": (
        b"BSJB\x00\xc3",
        ASSEMBLY + KEYLOG + RUN_KEY,
        set(),
        {PERSISTED},
    ),
    # Plain assembly with none of the behavior legs: must stay silent.
    "benign-assembly.exe": (
        b"BSJB\x00\xc3",
        ASSEMBLY,
        set(),
        {PERSISTED},
    ),
}


def matched_ids(cleave: str, target: Path) -> set:
    proc = subprocess.run(
        [cleave, "--traits-dir", str(ROOT), "--format", "json", str(target)],
        capture_output=True, text=True, check=True,
    )
    doc = json.loads(proc.stdout)
    ids = set()
    for scanned in doc["files"]:
        ids.update(t["id"] for t in scanned["traits"])
    return ids


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cleave", default="cleave")
    args = parser.parse_args()

    failed = False
    with tempfile.TemporaryDirectory(prefix="dotnet-persisted-") as tmp:
        for name, (text, rdata, want, reject) in FIXTURES.items():
            target = Path(tmp) / name
            target.write_bytes(pe32(text, rdata))
            ids = matched_ids(args.cleave, target)
            for trait in want:
                if trait not in ids:
                    print(f"FAIL {name}: expected {trait}")
                    failed = True
            for trait in reject:
                if trait in ids:
                    print(f"FAIL {name}: unexpected {trait}")
                    failed = True
    if failed:
        sys.exit(1)
    print("persisted polling-keylogger exfiltration checks passed")


if __name__ == "__main__":
    main()
