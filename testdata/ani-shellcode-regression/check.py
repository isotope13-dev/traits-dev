#!/usr/bin/env python3
"""Exercise inline YARA, which the broad `cleave validate` corpus disables."""
import json
import os
from pathlib import Path
import struct
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get("CLEAVE", str(ROOT.parent / "cleave/target/release/cleave"))
MEMORY = "objectives/execution/exploit/memory::"
DROPPER = "objectives/command-and-control/dropper/file-exec/shellcode::"
HASHING = "objectives/anti-static/obfuscation/imports/api-hashing::"
RAW = {MEMORY + "ani-duplicate-header-overflow", DROPPER + "ani-overflow-download-launch-shellcode", HASHING + "ani-overflow-hashed-api-shellcode"}
XOR = {MEMORY + "ani-overflow-xor-code-staging", DROPPER + "ani-xor-download-launch-shellcode", HASHING + "ani-xor-hashed-api-shellcode"}


def main():
    raw = (ROOT / "testdata/hostile/ani-raw-shellcode-controls/raw-download-launch.ani").read_bytes()
    encoded = (Path(__file__).parent / "xor-download-launch.ani").read_bytes()
    length_variant = bytearray(raw)
    struct.pack_into("<I", length_variant, 84, 100)
    key_variant = bytearray(encoded)
    loop = encoded.index(bytes.fromhex("80301d40e2fa"))
    key_variant[loop + 2] = 0x2a
    for i in range(247, 505):
        key_variant[i] ^= 0x1d ^ 0x2a
    mismatch = bytearray(encoded)
    mismatch[loop + 2] = 0x2a
    variants = {"renamed.wav": raw, "changed-length.bin": length_variant,
                "xor.bin": encoded, "changed-key.bin": key_variant,
                "mismatched-key.bin": mismatch}
    with tempfile.TemporaryDirectory(prefix="ani-regression-") as tmp:
        folder = Path(tmp)
        for name, data in variants.items():
            (folder / name).write_bytes(data)
        command = [CLEAVE, "--traits-dir", str(ROOT), "--json", str(folder),
                   str(ROOT / "testdata/benign/ani-structure-controls")]
        env = dict(os.environ)
        env.setdefault("CLEAVE_SKIP_CACHE", "1")
        env.setdefault("CLEAVE_SKIP_MAPPER_CACHE", "1")
        result = subprocess.run(command, capture_output=True, text=True, check=True, env=env)
        reports = [f for line in result.stdout.splitlines()
                   for f in json.loads(line)["files"]]
        assert len(reports) == 10, len(reports)
        for report in reports:
            name = Path(report["path"]).name
            hostile = {t["id"] for t in report.get("traits", []) if t["crit"] == 5}
            severe = {t["id"] for t in report.get("traits", []) if t["crit"] >= 4}
            if name in {"renamed.wav", "changed-length.bin"}:
                assert RAW <= hostile, (name, hostile)
            elif name in {"xor.bin", "changed-key.bin"}:
                assert XOR <= hostile, (name, hostile)
            elif name == "mismatched-key.bin":
                assert not hostile and not (XOR & severe), (name, severe)
            else:
                assert not severe, (name, severe)
        print(json.dumps({"cases": len(reports), "status": "pass"}))


if __name__ == "__main__":
    main()
