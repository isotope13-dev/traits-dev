#!/usr/bin/env python3
"""Exercise behavior boundaries using supplied specimens and inert PE controls."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import lzma
from pathlib import Path
import struct
import subprocess

ap = argparse.ArgumentParser()
ap.add_argument("--collector", type=Path, required=True)
ap.add_argument("--client", type=Path, required=True)
ap.add_argument("--file-manager", type=Path, required=True)
ap.add_argument("--output", type=Path, required=True)
ap.add_argument("--cleave", default="cleave")
args = ap.parse_args()
args.output.mkdir(parents=True, exist_ok=True)
root = Path(__file__).resolve().parents[3]
K = "objectives/collection/keylog/hook::managed-bank-page-keylogger"
E = "objectives/exfiltration/stealer/multi-source::managed-bank-capture-smtp"
I = "objectives/impact/infect/virus::managed-delimited-exe-prepender"
checks = []
data = args.collector.read_bytes()
checks.append((args.collector, {K, E, I}, set()))
mutations = [
    ("no-bank-targets", [(t.encode("utf-16le"), b"X\0" * len(t)) for t in
                        ["پرداخت اینترنتی", "مشخصات کارت",
                         "بانکداری اینترنتی", "بانکداري اينترنتي"]],
     {I}, {K, E}),
    ("no-key-record", [(b"IsDigit\0", b"IsAlpha\0")], {I}, {K, E}),
    ("no-hook-install", [(b"SetWindowsHookEx\0", b"GetWindowsHookEx\0")],
     {I}, {K, E}),
    ("no-smtp-client", [(b"SmtpClient\0", b"NullClient\0")], {K, I}, {E}),
    ("no-byte-splice-write", [(b"WriteByte\0", b"CopyBytes\0")],
     {K, E}, {I}),
]
for name, edits, required, forbidden in mutations:
    changed = data
    for old, new in edits:
        assert len(old) == len(new) and old in changed, (name, old)
        changed = changed.replace(old, new)
    path = args.output / (name + ".exe")
    path.write_bytes(changed)
    checks.append((path, required, forbidden))

def inert_pe(content):
    """RET entry followed by unexecuted test bytes in a readable .text section."""
    size = (len(content) + 1 + 511) // 512 * 512
    b = bytearray(512 + size)
    b[:2] = b"MZ"
    struct.pack_into("<I", b, 0x3c, 0x80)
    b[0x80:0x84] = b"PE\0\0"
    struct.pack_into("<HHIIIHH", b, 0x84, 0x14c, 1, 0, 0, 0, 224, 0x102)
    o = 0x98
    struct.pack_into("<H", b, o, 0x10b)
    for offset, value in {4: size, 16: 4096, 20: 4096, 28: 0x400000,
                          32: 4096, 36: 512, 56: 4096 + ((size+4095)//4096)*4096,
                          60: 512, 92: 16}.items():
        struct.pack_into("<I", b, o + offset, value)
    struct.pack_into("<H", b, o+68, 2)
    sec = o + 224
    b[sec:sec+8] = b".text\0\0\0"
    struct.pack_into("<IIII", b, sec+8, size, 4096, size, 512)
    struct.pack_into("<I", b, sec+36, 0x60000020)
    b[512] = 0xc3
    b[513:513+len(content)] = content
    return bytes(b)

L = {f"metadata/file/magic/numbers::lzma-sized-nonzero-{i}" for i in (1, 2, 3)}
for i, length in enumerate((16, 1024, 65536), 1):
    payload = b"A" * length
    packed = lzma.compress(payload, format=lzma.FORMAT_ALONE)
    sized = packed[:5] + struct.pack("<Q", length) + packed[13:]
    assert lzma.decompress(sized, format=lzma.FORMAT_ALONE) == payload
    path = args.output / f"lzma-size-byte-{i}.exe"
    path.write_bytes(inert_pe(sized))
    checks.append((path, {f"metadata/file/magic/numbers::lzma-sized-nonzero-{i}"},
                   L - {f"metadata/file/magic/numbers::lzma-sized-nonzero-{i}"}))
    damaged = sized[:12] + b"\1" + sized[13:]  # implausible high size byte
    path = args.output / f"lzma-high-size-nearmiss-{i}.exe"
    path.write_bytes(inert_pe(damaged))
    checks.append((path, set(), L))
path = args.output / "clr-table-lookalike.exe"
path.write_bytes(inert_pe(bytes.fromhex("5d00000100290114cb000000008100")))
checks.append((path, set(), L))

for path in (args.client, args.file_manager):
    checks.append((path, {"well-known/dual-use/remote-admin/screenconnect::screenconnect-family"},
                   {K, E, I} | L))

def check(case):
    path, required, forbidden = case
    cp = subprocess.run([args.cleave, "--traits-dir", str(root), "--format", "json",
                         str(path)], text=True, capture_output=True, check=True)
    report = json.loads(cp.stdout)
    ids = {t["id"] for f in report["files"] for t in f.get("traits", [])}
    assert required <= ids, (path.name, "missing", sorted(required - ids))
    assert not forbidden & ids, (path.name, "unexpected", sorted(forbidden & ids))
    if path in (args.client, args.file_manager):
        assert not [(f["path"], t["id"]) for f in report["files"]
                    for t in f.get("traits", []) if t["crit"] >= 4]
    return {"case": path.name, "passed": True,
            "required": sorted(required), "forbidden": sorted(forbidden)}
with ThreadPoolExecutor(max_workers=3) as pool:
    results = list(pool.map(check, checks))
(args.output.parent / "controls-results.json").write_text(json.dumps(results, indent=2))
print(f"{len(results)} behavior, identity, and LZMA controls passed")

