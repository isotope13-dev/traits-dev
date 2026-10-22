#!/usr/bin/env python3
"""Check the DOS interpreter-target binding without running DOS code.

Usage: python3 check.py /path/to/the/Radish-memory-image
"""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[3]
ENGINE = os.environ.get("CLEAVE", "cleave")
HOSTILE = "objectives/impact/infect/binary/dos/overwrite::dos-command-interpreter-image-overwrite"
CREATE = "micro-behaviors/fs/file/create::dos-jump-padded-create-image-write"
TARGET = "micro-behaviors/fs/file/create::dos-command-com-create-target"
JUNK = "objectives/anti-static/obfuscation/instruction/junk::dos-jump-skipped-nop-register-save"
FONT = "micro-behaviors/ui/graphics/font::bios-load-custom-font-block"
RULES = {HOSTILE, CREATE, TARGET, JUNK, FONT}


def scan(path):
    result = subprocess.run(
        [ENGINE, "--traits-dir", str(ROOT), "--format", "json", str(path)],
        capture_output=True, text=True, check=True,
    )
    report = json.loads(result.stdout)
    return {t["id"] for f in report["files"] for t in f.get("traits", [])}


sample = Path(sys.argv[1]).read_bytes()
assert sample[0x100:0x104] == bytes.fromhex("9c eb 01 90")
assert sample[0x21d5:0x21e3] == b"c:\\command.com"
wrong_target = bytearray(sample)
# Keep the COMMAND.COM text, but point DOS's create call one byte past it.
wrong_target[0x11d:0x11f] = (0x21d6).to_bytes(2, "little")
no_write = bytearray(sample)
no_write[0x137] = 0x3f  # AH=read rather than AH=write
no_font = bytearray(sample)
no_font[0x1cf] = 0       # AX=1100h, not the matched 1110h operation
for name, content, expected in [
    ("memory-image", sample, RULES),
    ("psp-stripped", sample[256:], RULES),
    ("unrelated-command-path", wrong_target, {CREATE, JUNK, FONT}),
    ("without-image-write", no_write, {TARGET, JUNK, FONT}),
    ("without-font-operation", no_font, RULES - {FONT}),
]:
    with tempfile.TemporaryDirectory(prefix=".controls-", dir=Path(__file__).parent) as temp:
        path = Path(temp, name + ".com")
        path.write_bytes(content)
        actual = scan(path) & RULES
        assert actual == expected, (name, expected, actual)
        print("PASS", name, flush=True)
