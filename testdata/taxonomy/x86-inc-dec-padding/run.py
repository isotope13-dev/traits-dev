#!/usr/bin/env python3
"""Exercise register pairing, repetition, architecture and section boundaries."""
import argparse
import json
from pathlib import Path
import struct
import subprocess
import tempfile

TRAIT = "objectives/anti-static/obfuscation/instruction/junk::x86-long-byte-inc-dec-padding"


def image(code, *, bits=32, executable=True, raw_size=512):
    header_size = 240 if bits == 64 else 224
    data = bytearray(1024)
    data[:2] = b"MZ"
    struct.pack_into("<I", data, 0x3c, 0x80)
    data[0x80:0x84] = b"PE\0\0"
    struct.pack_into("<HHIIIHH", data, 0x84,
                     0x8664 if bits == 64 else 0x14c, 1, 0, 0, 0,
                     header_size, 0x22 if bits == 64 else 0x102)
    opt = 0x98
    struct.pack_into("<H", data, opt, 0x20b if bits == 64 else 0x10b)
    struct.pack_into("<I", data, opt + 16, 0x1000)
    struct.pack_into("<I", data, opt + 20, 0x1000)
    if bits == 64:
        struct.pack_into("<Q", data, opt + 24, 0x140000000)
    else:
        struct.pack_into("<I", data, opt + 28, 0x400000)
    struct.pack_into("<II", data, opt + 32, 0x1000, 0x200)
    struct.pack_into("<II", data, opt + 56, 0x2000, 0x200)
    struct.pack_into("<H", data, opt + 68, 3)
    section = opt + header_size
    data[section:section + 8] = b".code\0\0\0" if executable else b".data\0\0\0"
    struct.pack_into("<IIII", data, section + 8, raw_size, 0x1000, raw_size, 0x200)
    struct.pack_into("<I", data, section + 36, 0x60000020 if executable else 0x40000040)
    data[512:512 + len(code)] = code
    return data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cleave", default="cleave")
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[3]
    cases = {}
    for bits in (32, 64):
        for reg in range(8):
            for reverse in (False, True):
                pair = bytes((0xfe, 0xc0 + reg, 0xfe, 0xc8 + reg))
                if reverse:
                    pair = pair[2:] + pair[:2]
                name = f"reg{reg}-{bits}-reverse{int(reverse)}"
                cases[name] = (image(pair * 32 + b"\xc3", bits=bits), True)
    pair = bytes.fromhex("fe c1 fe c9")
    cases["short-run"] = (image(pair * 31 + b"\xc3"), False)
    cases["different-registers"] = (image(bytes.fromhex("fe c1 fe ca") * 64), False)
    cases["interrupted"] = (image(pair * 16 + b"\x90" + pair * 16), False)
    cases["non-executable-data"] = (image(pair * 64, executable=False), False)
    cases["cross-section-end"] = (image(b"\x90" * 64 + pair * 32, raw_size=128), False)
    cases["ordinary-return"] = (image(b"\xc3"), False)
    with tempfile.TemporaryDirectory(prefix="fixtures-", dir=Path(__file__).parent) as tmp:
        for name, (data, _) in cases.items():
            Path(tmp, name + ".exe").write_bytes(data)
        proc = subprocess.run([args.cleave, "--traits-dir", str(repo), "--format", "json", tmp],
                              check=True, capture_output=True, text=True)
        # Directory analysis can concatenate JSON documents without delimiters.
        decoder = json.JSONDecoder()
        reports = []
        remaining = proc.stdout.strip()
        while remaining:
            report, end = decoder.raw_decode(remaining)
            reports.append(report)
            remaining = remaining[end:].lstrip()
        seen = set()
        files = [file for report in reports for file in report.get("files", [report])]
        for file in files:
            name = Path(file["path"]).stem
            if name not in cases:
                continue
            seen.add(name)
            actual = any(t["id"] == TRAIT for t in file["traits"])
            assert actual == cases[name][1], (name, actual, cases[name][1])
        assert seen == set(cases), set(cases) - seen
    print(f"Passed {len(cases)} positive and near-miss controls")


if __name__ == "__main__":
    main()
