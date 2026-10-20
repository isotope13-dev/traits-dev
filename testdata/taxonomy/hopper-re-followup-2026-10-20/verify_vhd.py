"""Generate harmless VHD controls and verify extraction and capacity limits.

Requires a Cleave build with sibling filefacts VHD support and system 7-Zip.
No real malware fixtures or mounted filesystems are used.
"""
import argparse
import json
import struct
import subprocess
import tempfile
from pathlib import Path


def footer(data, kind, size):
    f = memoryview(data)[-512:]
    f[:8] = b"conectix"
    struct.pack_into(">IIQ", f, 8, 2, 0x10000, (1 << 64) - 1 if kind == 2 else 512)
    f[28:32] = b"test"
    struct.pack_into(">QQ", f, 40, size, size)
    struct.pack_into(">I", f, 60, kind)
    struct.pack_into(">I", f, 64, (~sum(f)) & 0xffffffff)


def fixed_fat12():
    b = bytearray(2880 * 512 + 512)
    b[:3] = b"\xeb\x3c\x90"
    b[3:11] = b"MSDOS5.0"
    struct.pack_into("<HBHBHHBHHHII", b, 11, 512, 1, 1, 2, 224, 2880, 0xf0, 9, 18, 2, 0, 0)
    b[38] = 0x29
    b[43:54] = b"TEST VOLUME"
    b[54:62] = b"FAT12   "
    b[510:512] = b"\x55\xaa"
    for at in [512, 10 * 512]:
        b[at:at + 6] = bytes.fromhex("f0ffffff0f00")
    a = 19 * 512
    b[a:a + 11] = b"HELLO   TXT"
    b[a + 11] = 0x20
    struct.pack_into("<H", b, a + 26, 2)
    struct.pack_into("<I", b, a + 28, 12)
    b[33 * 512:33 * 512 + 12] = b"hello world\n"
    footer(b, 2, 2880 * 512)
    return b


def oversized_sparse():
    b = bytearray(2048)
    b[512:520] = b"cxsparse"
    struct.pack_into(">I", b, 536, 0x10000)
    footer(b, 3, 1 << 48)
    return b


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--cleave", type=Path, required=True)
    ap.add_argument("--traits-dir", type=Path, required=True)
    args = ap.parse_args()
    with tempfile.TemporaryDirectory(prefix="vhd-controls-") as directory:
        small, large = [Path(directory) / n for n in ["small.vhd", "large.vhd"]]
        small.write_bytes(fixed_fat12())
        large.write_bytes(oversized_sparse())
        run = subprocess.run(
            [str(args.cleave.resolve()), "--traits-dir", str(args.traits_dir.resolve()), "--json", str(small), str(large)],
            check=True, capture_output=True, text=True, timeout=120,
        )
        files = [f for line in run.stdout.splitlines() for f in json.loads(line).get("files", [])]
        by_path = {f["path"]: f for f in files}
        assert by_path[str(small)]["type"] == "vhd"
        assert by_path[str(small) + "!!HELLO.TXT"]["size"] == 12
        assert by_path[str(large)]["type"] == "vhd"
        assert any(t["id"] == "anti-analysis/archive/excessive-size" for t in by_path[str(large)]["traits"])
        assert not any(p.startswith(str(large) + "!!") for p in by_path)
    print(json.dumps({"fixed_vhd_file_extraction": "passed", "sparse_vhd_capacity_guard": "passed"}))


if __name__ == "__main__":
    main()
