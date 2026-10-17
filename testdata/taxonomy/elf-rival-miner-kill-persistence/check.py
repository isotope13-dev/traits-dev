#!/usr/bin/env python3
"""Native ELF rival-miner kill list and unit+crontab persistence.

Builds minimal non-executable AArch64 ELF fixtures (named sections, no
entry point) and checks the two hostile composites covering the
boatnet-style cryptojacker: a kill-syscall plus three-or-more rival
miner names, and an embedded systemd unit plus piped crontab install
under a kworker process title.

Covers the needs:3 threshold (two miner names must not fire the kill
list) and the all-legs requirement of the persistence composite (a
unit template alone must not fire it).
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

KILL = ("objectives/impact/degrade/rival-bot/competitor::"
        "elf-rival-miner-process-kill-list")
PERSIST = ("objectives/persistence/system/service/systemd::"
           "elf-unit-crontab-kworker-persistence")

# movz x8, #129 (aarch64 __NR_kill); svc #0; ret.
KILL_CODE = bytes.fromhex("281080d2" "010000d4" "c0035fd6")
RET_CODE = bytes.fromhex("c0035fd6")

UNIT = (b"[Service]\nType=simple\nExecStart=\n"
        b"WantedBy=multi-user.target\n")


def elf64(rodata: bytes, code: bytes) -> bytes:
    """Minimal relocatable AArch64 ELF: non-executable fixture."""
    names = b"\0.text\0.rodata\0.shstrtab\0"
    textoff = 64
    rodoff = (textoff + len(code) + 15) & ~15
    nameoff = rodoff + len(rodata)
    shoff = (nameoff + len(names) + 15) & ~15
    data = bytearray(shoff + 4 * 64)
    ident = b"\x7fELF\x02\x01\x01" + bytes(9)
    data[:64] = struct.pack("<16sHHIQQQIHHHHHH", ident, 1, 183, 1, 0, 0,
                            shoff, 0, 64, 0, 0, 64, 4, 0)
    data[textoff:textoff + len(code)] = code
    data[rodoff:rodoff + len(rodata)] = rodata
    data[nameoff:nameoff + len(names)] = names
    for index, name, flags, offset, size in [
        (1, 1, 6, textoff, len(code)),
        (2, 7, 2, rodoff, len(rodata)),
        (3, 15, 0, nameoff, len(names)),
    ]:
        data[shoff + index * 64:shoff + (index + 1) * 64] = struct.pack(
            "<IIQQQQIIQQ", name, 1 if index < 3 else 3, flags,
            0, offset, size, 0, 0, 1, 0)
    return bytes(data)


FIXTURES = {
    # Kill syscall, four rival miner names, unit template, piped crontab
    # install, kworker title: both composites fire.
    "rival-kill-unit-cron.elf": (
        KILL_CODE,
        b"xmrig\0cpuminer\0minerd\0[kworker/1:1]\0" + UNIT +
        b"(crontab -l 2>/dev/null; echo '*/15 * * * * /tmp/.x') | crontab -\n",
        {KILL, PERSIST},
        set(),
    ),
    # Kill syscall but only two miner names: kill list must stay silent.
    "near-miss-two-names.elf": (
        KILL_CODE,
        b"xmrig\0cpuminer\0",
        set(),
        {KILL, PERSIST},
    ),
    # Unit template without crontab install, kworker title, or miner
    # names: persistence composite must stay silent.
    "benign-unit-installer.elf": (
        RET_CODE,
        b"Restart=always\n" + UNIT,
        set(),
        {KILL, PERSIST},
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
    with tempfile.TemporaryDirectory(prefix="elf-rival-kill-") as tmp:
        for name, (code, rodata, want, reject) in FIXTURES.items():
            target = Path(tmp) / name
            target.write_bytes(elf64(rodata, code))
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
    print("rival-miner kill list and unit+crontab persistence checks passed")


if __name__ == "__main__":
    main()
