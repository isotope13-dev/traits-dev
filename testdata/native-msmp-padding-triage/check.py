#!/usr/bin/env python3
"""Generate inert PE controls and check the MSMP/padding observations."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import os
from pathlib import Path
import re
import struct
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
COMPLEMENT = bytes.fromhex(
    "33 C0 8A 4C 04 08 F6 D1 88 4C 04 08 40 3D 00 02 00 00 72 EE"
)
MAGIC = bytes.fromhex("81 7C 24 08 4D 53 4D 50")
LOOP_ID = "micro-behaviors/data/arithmetic::x86-byte-complement-512"
MAGIC_ID = "well-known/malware/trojan/urelas::msmp-state-compare-x86"
ALPHA_ID = "metadata/file/profile/string-population::native-long-alphabetic-strings"
OVERLAY_ID = "metadata/binary/layout/overlay::adginpx-overlay-run"
SMALL_ID = "metadata/binary/layout/overlay::small-pe-adginpx-overlay-run"
FAMILY_IDS = {
    "well-known/malware/trojan/urelas::urelas-msmp-network-loader",
    "well-known/malware/trojan/urelas::urelas-msmp-disk-path-network-loader",
}
IDS = {LOOP_ID, MAGIC_ID, ALPHA_ID, OVERLAY_ID, SMALL_ID} | FAMILY_IDS


def pe(code=b"\xc3", data=b"", overlay=b""):
    """A minimal 32-bit image; controls are analyzed, never executed."""
    b = bytearray(0x8200)
    b[:2] = b"MZ"
    struct.pack_into("<I", b, 0x3C, 0x80)
    b[0x80:0x84] = b"PE\0\0"
    struct.pack_into("<HHIIIHH", b, 0x84, 0x14C, 2, 0, 0, 0, 0xE0, 0x102)
    opt = 0x98
    struct.pack_into("<H", b, opt, 0x10B)
    struct.pack_into("<I", b, opt + 16, 0x1000)
    struct.pack_into("<III", b, opt + 28, 0x400000, 0x1000, 0x200)
    struct.pack_into("<II", b, opt + 56, 0xA000, 0x200)
    struct.pack_into("<H", b, opt + 68, 3)
    struct.pack_into("<I", b, opt + 92, 16)
    for idx, (name, va, offset, size, flags) in enumerate([
        (b".text", 0x1000, 0x200, 0x2000, 0x60000020),
        (b".data", 0x4000, 0x2200, 0x6000, 0xC0000040),
    ]):
        hdr = opt + 0xE0 + idx * 40
        struct.pack_into("<8sIIIIIIHHI", b, hdr, name, size, va, size, offset,
                         0, 0, 0, 0, flags)
    b[0x200:0x200 + len(code)] = code
    b[0x2200:0x2200 + len(data)] = data
    return bytes(b) + overlay


def check(engine, path, required, forbidden):
    env = dict(os.environ, CLEAVE_TRAITS_DIR=str(ROOT))
    run = subprocess.run([engine, "test-rules", str(path), "--rules",
                          ",".join(sorted(IDS))], env=env, text=True,
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         check=True)
    if "validation failed" in run.stdout or re.search(r"Warning: Rule .*not found", run.stdout):
        raise AssertionError(run.stdout)
    matched = set(re.findall(r"^MATCHED (\S+)", run.stdout, re.MULTILINE))
    assert required <= matched, (path.name, "missing", required - matched)
    assert not forbidden & matched, (path.name, "unexpected", forbidden & matched)
    print("PASS", path.name, flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cleave", default=os.environ.get("CLEAVE", "cleave"))
    parser.add_argument("--sample", type=Path,
                        help="Optional Urelas specimen for mutation controls")
    args = parser.parse_args()
    cases = [
        ("complement-and-msmp.exe", pe(COMPLEMENT + MAGIC),
         {LOOP_ID, MAGIC_ID}, FAMILY_IDS),
        ("different-buffer.exe", pe(COMPLEMENT[:11] + b"\x09" + COMPLEMENT[12:]),
         set(), {LOOP_ID} | FAMILY_IDS),
        ("different-length.exe", pe(COMPLEMENT.replace(b"\x00\x02\x00\x00",
                                                        b"\xff\x01\x00\x00")),
         set(), {LOOP_ID} | FAMILY_IDS),
        ("data-is-not-code.exe", pe(data=COMPLEMENT + MAGIC),
         set(), {LOOP_ID, MAGIC_ID} | FAMILY_IDS),
        ("alphabetic-padding.exe", pe(data=b"AbCdEfGhJkLmNpQrStUvWxYz" * 60 + b"\0" +
                                       b"mnopqrstuvwXYZABCDEFghijk" * 60,
                                       overlay=b"ADGINPX" * 74),
         {ALPHA_ID, OVERLAY_ID, SMALL_ID}, FAMILY_IDS),
        ("short-padding.exe", pe(data=b"j" * 999 + b"\0" + b"F" * 999,
                                  overlay=b"G" * 255),
         set(), {ALPHA_ID, OVERLAY_ID, SMALL_ID} | FAMILY_IDS),
        ("installer-padding.exe", pe(overlay=b"PADDINGXX" * 100),
         set(), {OVERLAY_ID, SMALL_ID} | FAMILY_IDS),
    ]
    if args.sample:
        original = args.sample.read_bytes()
        renamed = original
        for name in ("HGDraw.dll", "golfinfo.ini"):
            renamed = renamed.replace(name.encode("utf-16le"),
                                      ("x" * len(name)).encode("utf-16le"))
        cases.extend([
            ("original.exe", original, FAMILY_IDS | {ALPHA_ID, OVERLAY_ID}, set()),
            ("renamed-artifacts.exe", renamed, FAMILY_IDS, set()),
            ("no-msmp-magic.exe", original.replace(b"MSMP", b"ABCD"),
             set(), FAMILY_IDS | {MAGIC_ID}),
            ("no-complement.exe", original.replace(COMPLEMENT, b"\x90" * len(COMPLEMENT)),
             set(), FAMILY_IDS | {LOOP_ID}),
        ])
    with tempfile.TemporaryDirectory(prefix="native-msmp-controls-") as tmp:
        def run(case):
            name, content, required, forbidden = case
            path = Path(tmp) / name
            path.write_bytes(content)
            check(args.cleave, path, required, forbidden)

        with ThreadPoolExecutor(max_workers=3) as pool:
            list(pool.map(run, cases))


if __name__ == "__main__":
    main()
