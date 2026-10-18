#!/usr/bin/env python3
"""Synthetic PE controls for POST buffer binding and bounded header scanning."""
import argparse
import json
from pathlib import Path
import struct
import subprocess
import tempfile


POST = "micro-behaviors/communications/http/direct-socket::x86-formatted-post-buffer-send"
SCAN = "micro-behaviors/data/format/pe-parser::mz-nop-header-scan"
FLOW = bytes.fromhex(
    "6a10 8d85 54fcffff 50 ffb5 68fdffff e8 00000000 83f8ff 0f84 00000000 "
    "ff750c ff750c ff15 00304000 50 8d85 6cfdffff 50 8d85 68fcffff 50 "
    "68 00204000 ffb5 6cfeffff ff15 04304000 83c418 "
    "68e8030000 ff15 08304000 "
    "6a00 ffb5 6cfeffff ff15 0c304000 40 50 "
    "ffb5 6cfeffff ffb5 68fdffff e8 00000000"
)
REQUEST = b"POST %s HTTP/1.1\r\nHost: %s\r\n\r\n%s\0WS2_32.dll\0"
LOOP = bytes.fromhex("81384d5a9000 740c 4041 81f9 f4010000 7cee")


def pe(code, data=REQUEST, image_base=0x400000):
    """Build two sections without imports, payloads, or runnable API targets."""
    blob = bytearray(0x600)
    blob[:2] = b"MZ"
    struct.pack_into("<I", blob, 0x3C, 0x80)
    blob[0x80:0x84] = b"PE\0\0"
    struct.pack_into("<HHIIIHH", blob, 0x84, 0x14C, 2, 0, 0, 0, 224, 0x102)
    opt = 0x98
    struct.pack_into("<H", blob, opt, 0x10B)
    for offset, value in {16: 0x1000, 20: 0x1000, 24: 0x2000,
                          28: image_base, 32: 0x1000, 36: 0x200,
                          56: 0x3000, 60: 0x200, 92: 16}.items():
        struct.pack_into("<I", blob, opt + offset, value)
    struct.pack_into("<H", blob, opt + 68, 3)
    for index, (name, rva, raw, flags) in enumerate([
        (b".text", 0x1000, 0x200, 0x60000020),
        (b".rdata", 0x2000, 0x400, 0x40000040),
    ]):
        struct.pack_into("<8sIIIIIIHHI", blob, opt + 224 + index * 40,
                         name, 0x200, rva, 0x200, raw, 0, 0, 0, 0, flags)
    blob[0x200:0x200 + len(code)] = code
    blob[0x400:0x400 + len(data)] = data
    return blob


def change(blob, offset, value):
    result = bytearray(blob)
    struct.pack_into("<I", result, offset, value)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cleave", default="cleave")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    relocated = change(FLOW, 57, 0x502010)
    for offset in (63, len(FLOW) - 29, len(FLOW) - 15):
        relocated = change(relocated, offset, 0xFFFFFE40)
    for offset in (11, len(FLOW) - 9):
        relocated = change(relocated, offset, 0xFFFFFD40)
    cases = {
        "post-sender": (pe(FLOW), POST, True),
        "relocated-sender": (pe(relocated, b"\0" * 16 + REQUEST, 0x500000), POST, True),
        "wrong-format-pointer": (pe(change(FLOW, 57, 0x402001)), POST, False),
        "different-transmit-buffer": (pe(change(FLOW, len(FLOW) - 15, 0xFFFFFE70)), POST, False),
        "different-socket": (pe(change(FLOW, len(FLOW) - 9, 0xFFFFFD70)), POST, False),
        "request-template-only": (pe(b"\xc3"), POST, False),
        "without-winsock": (pe(FLOW, REQUEST.replace(b"WS2_32.dll", b"ordinary!!")), POST, False),
        "bounded-header-scan": (pe(LOOP, b""), SCAN, True),
        "header-compare-only": (pe(LOOP[:6] + b"\xc3", b""), SCAN, False),
        "without-backedge": (pe(LOOP[:-2] + b"\x90\x90", b""), SCAN, False),
    }
    with tempfile.TemporaryDirectory(prefix="native-post-controls-") as temp:
        for name, (blob, _, _) in cases.items():
            (Path(temp) / (name + ".exe")).write_bytes(blob)
        result = subprocess.run([args.cleave, "--traits-dir", str(root),
                                 "--format", "json", temp],
                                text=True, capture_output=True, check=True)
        reports = []
        remaining = result.stdout.lstrip()
        while remaining:
            document, end = json.JSONDecoder().raw_decode(remaining)
            reports.extend(document["files"])
            remaining = remaining[end:].lstrip()
        assert len(reports) == len(cases), len(reports)
        for report in reports:
            name = Path(report["path"]).stem
            _, trait, expected = cases[name]
            ids = {item["id"] for item in report["traits"]}
            assert (trait in ids) == expected, (name, trait, ids)
            assert not any(item["crit"] == 5 for item in report["traits"]), name
            print(f"PASS {name}: expected {expected}")


if __name__ == "__main__":
    main()
