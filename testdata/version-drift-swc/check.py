"""Focused matcher controls; generated images are inert and never executed.

Run: python3 testdata/version-drift-swc/check.py <scratch-directory>
The review also compares two original SWC releases and two original malicious
loaders. These small controls check instruction operands, thresholds, record
boundaries, and symbol-versus-string matching, rather than replacing that audit.
"""
import json
import os
from pathlib import Path
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
TLS = "objectives/anti-static/obfuscation/control-flow/dispatch::tls-state-relative-table-flattening"
QUERY = "micro-behaviors/communications/socket/udp::game-query-data-section-bytes"
BROTLI = "micro-behaviors/data/decompress/brotli::native-brotli-decompress-symbol"


def align(n, boundary):
    return (n + boundary - 1) // boundary * boundary


def pe(code=b"\xc3", data=b"\0", export=None):
    code = code.ljust(align(len(code), 512), b"\xcc")
    data_rva = align(0x1000 + len(code), 4096)
    if export:
        exports = bytearray(256)
        struct.pack_into("<IIHHIIIIIII", exports, 0, 0, 0, 0, 0,
                         data_rva + 192, 1, 1, 1, data_rva + 64,
                         data_rva + 68, data_rva + 72)
        struct.pack_into("<IIH", exports, 64, 0x1000, data_rva + 128, 0)
        name = export.encode() + b"\0"
        exports[128:128+len(name)] = name
        exports[192:204] = b"fixture.dll\0"
        data = bytes(exports) + data
    raw_data_size = align(len(data), 512)
    header = bytearray(512)
    header[:2] = b"MZ"
    struct.pack_into("<I", header, 0x3c, 0x80)
    header[0x80:0x84] = b"PE\0\0"
    struct.pack_into("<HHIIIHH", header, 0x84, 0x8664, 2, 0, 0, 0, 240, 0x2022)
    opt = 0x98
    struct.pack_into("<H", header, opt, 0x20b)
    struct.pack_into("<I", header, opt+16, 0x1000)
    struct.pack_into("<Q", header, opt+24, 0x140000000)
    struct.pack_into("<II", header, opt+32, 4096, 512)
    struct.pack_into("<II", header, opt+56, align(data_rva+raw_data_size, 4096), 512)
    struct.pack_into("<H", header, opt+68, 3)
    struct.pack_into("<I", header, opt+108, 16)
    if export:
        struct.pack_into("<II", header, opt+112, data_rva, 256)
    for off, name, size, rva, raw, flags in [
        (0x188, b".text", len(code), 0x1000, 512, 0x60000020),
        (0x1b0, b".rdata", raw_data_size, data_rva, 512+len(code), 0x40000040),
    ]:
        struct.pack_into("<8sIIIIIIHHI", header, off, name, size, rva,
                         size, raw, 0, 0, 0, 0, flags)
    return bytes(header) + code + data.ljust(raw_data_size, b"\0")


def elf(data):
    names = b"\0.rodata\0.shstrtab\0"
    stroff = 64 + len(data)
    shoff = align(stroff + len(names), 8)
    header = struct.pack("<16sHHIQQQIHHHHHH", b"\x7fELF\x02\x01\x01" + bytes(9),
                         2, 62, 1, 0, 0, shoff, 0, 64, 0, 0, 64, 3, 2)
    def sh(name, kind, flags, offset, size):
        return struct.pack("<IIQQQQIIQQ", name, kind, flags, 0, offset, size, 0, 0, 1, 0)
    return ((header + data + names).ljust(shoff, b"\0") + bytes(64) +
            sh(1, 1, 2, 64, len(data)) + sh(9, 3, 0, stroff, len(names)))


def main():
    dest = Path(sys.argv[1])
    dest.mkdir(parents=True, exist_ok=True)
    # Original Ashusium window at file offset 0x188c: pointer CMOV followed
    # by an unindexed MOVSXD, a target-base LEA, ADD, and indirect JMP.
    pointer = bytes.fromhex(
        "654c8b1c2558000000 498b04c3 4c8b9898000000 488bf2 31c0 "
        "41ba00000000 4883ee05 4c0f43d6 4181c351a1ef1f 418bf3 483bd6 "
        "488d3de1600700 488d35be600700 480f42fe 48633f 488d352f010000 4801f7 ffe7")
    # Same nearby TLS read but an ordinary SIB-indexed enum-table load.
    indexed = pointer.replace(bytes.fromhex("48633f"), bytes.fromhex("48633c8e"))
    player = bytes.fromhex("ffffffff55ffffffff")
    table = b"\xff" * 48 + player + b"\xff" * 8 + b"\x55" * 24
    cases = {
        "five-pointer-dispatches.exe": (pe(code=pointer*5), {TLS}, set()),
        "four-pointer-dispatches.exe": (pe(code=pointer*4), set(), {TLS}),
        "tls-enum-switches.exe": (pe(code=indexed*12), set(), {TLS}),
        "no-tls-pointer-dispatches.exe": (pe(code=pointer.replace(b"\x65", b"\x90", 1)*5), set(), {TLS}),
        "brotli-export.exe": (pe(export="BrotliDecoderDecompressStream"), {BROTLI}, set()),
        "brotli-string.exe": (pe(data=b"BrotliDecoderDecompressStream\0"), set(), {BROTLI}),
        "brotli-state-export.exe": (pe(export="BrotliDecoderCreateInstance"), set(), {BROTLI}),
        "player-record.exe": (pe(data=b"\0"+player+b"\0"), {QUERY}, set()),
        "player-section-start.exe": (pe(data=player+b"\0"), {QUERY}, set()),
        "player-section-end.exe": (pe(data=bytes(503)+player), {QUERY}, set()),
        "player-lookup-table.exe": (pe(data=table), set(), {QUERY}),
        "named-query.exe": (pe(data=table+b"\0\xff\xff\xff\xffgetstatus\0"), {QUERY}, set()),
        "player-record.elf": (elf(player), {QUERY}, set()),
        "player-lookup-table.elf": (elf(table), set(), {QUERY}),
        "named-query.elf": (elf(b"\xff\xff\xff\xffTSource Engine Query\0"), {QUERY}, set()),
    }
    for name, (data, _, _) in cases.items():
        (dest/name).write_bytes(data)
    proc = subprocess.run([os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
                           "--format", "json", *[str(dest/name) for name in cases]],
                          check=True, capture_output=True, text=True)
    decoder = json.JSONDecoder()
    remaining = proc.stdout
    seen = {}
    while remaining.strip():
        report, end = decoder.raw_decode(remaining.lstrip())
        remaining = remaining.lstrip()[end:]
        for f in report["files"]:
            seen[Path(f["path"]).name] = {t["id"] for t in f.get("traits", [])}
    for name, (_, required, forbidden) in cases.items():
        assert required <= seen[name], (name, "missing", required-seen[name])
        assert not forbidden & seen[name], (name, "unexpected", forbidden & seen[name])
    print(f"{len(cases)} SWC version-drift controls passed")


if __name__ == "__main__":
    main()
