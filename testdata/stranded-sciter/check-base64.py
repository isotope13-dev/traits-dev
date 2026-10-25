#!/usr/bin/env python3
"""Check native inverse-Base64-table recognition without executing code."""
import argparse
import importlib.util
import json
from pathlib import Path
import struct
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
TRAIT = "micro-behaviors/data/encoding/base64::x86-inverse-alphabet-initialization"


def decoder(base=0x403000, padding=b"\x90"):
    address = struct.pack("<I", base)
    return (bytes.fromhex("b8410000008d48bf8888") + address
            + bytes.fromhex("4083f85a76f1b861000000") + padding
            + bytes.fromhex("8d50b98890") + address
            + bytes.fromhex("4083f87a76f1b8300000008d48048888") + address
            + bytes.fromhex("4083f83976f1c605")
            + struct.pack("<I", base + ord("+")) + b"\x3e\xc6\x05"
            + struct.pack("<I", base + ord("/")) + b"\x3f")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--scratch-dir", type=Path, required=True)
    args = parser.parse_args()
    spec = importlib.util.spec_from_file_location(
        "pe32", ROOT / "testdata/native-post-graft-review/run_cases.py")
    pe32 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pe32)
    code = decoder()
    wrong = code.replace(bytes.fromhex("8d50b9"), bytes.fromhex("8d50b8"))
    cases = {
        "inverse-table": (pe32.pe(b"\xc3" + code, b""), True),
        "relocated-no-padding": (pe32.pe(b"\xc3" + decoder(0x503000, b""), b""), True),
        "alignment-padding": (pe32.pe(b"\xc3" + decoder(padding=b"\x90" * 12), b""), True),
        "different-alphabet": (pe32.pe(b"\xc3" + wrong, b""), False),
        "missing-digit-loop": (pe32.pe(b"\xc3" + code[:43], b""), False),
        "data-section-only": (pe32.pe(b"\xc3", code), False),
        "name-and-alphabet-only": (pe32.pe(b"\xc3", b"fromBase64\0"
                                  b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/\0"), False),
    }
    with tempfile.TemporaryDirectory(dir=args.scratch_dir) as temp:
        for name, (blob, _) in cases.items():
            Path(temp, name + ".exe").write_bytes(blob)
        result = subprocess.run(
            ["cleave", "--traits-dir", str(ROOT), "--disable", "radare2",
             "--format", "json", temp], capture_output=True, text=True, check=True)
        remaining = result.stdout.lstrip()
        checked = set()
        while remaining:
            report, end = json.JSONDecoder().raw_decode(remaining)
            remaining = remaining[end:].lstrip()
            for file in report["files"]:
                name = Path(file["path"]).stem
                ids = {trait["id"] for trait in file.get("traits", [])}
                assert (TRAIT in ids) == cases[name][1], (name, ids)
                checked.add(name)
                print("PASS", name)
        assert checked == set(cases), checked


if __name__ == "__main__":
    main()
