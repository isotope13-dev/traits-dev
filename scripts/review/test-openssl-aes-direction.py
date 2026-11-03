#!/usr/bin/env python3
"""Check OpenSSL direction without excluding other commands in a file."""
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get("CLEAVE", "../cleave/target/release/cleave")
RULE = "micro-behaviors/crypto/encrypt/transform::openssl-aes-encrypt-command"

cases = {
    "default encryption": ("openssl enc -aes-256-cbc -in x -out y\n", True),
    "explicit encryption": ("openssl enc -e -aes-256-cbc -in x\n", True),
    "short decrypt option": ("openssl enc -aes-256-cbc -d -in x\n", False),
    "long decrypt option": ("openssl enc -decrypt -aes-256-cbc -in x\n", False),
    "separate commands": ("openssl enc -d -aes-256-cbc\nopenssl enc -aes-256-cbc\n", True),
    "same line commands": ("openssl enc -d -aes-256-cbc; openssl enc -aes-256-cbc\n", True),
}
with tempfile.TemporaryDirectory(prefix="openssl-aes-direction-") as directory:
    path = Path(directory) / "sample.sh"
    for name, (source, expected) in cases.items():
        path.write_text("#!/bin/sh\n" + source)
        result = subprocess.run(
            [CLEAVE, "--traits-dir", str(ROOT), "test-rules", "--rules", RULE, str(path)],
            cwd=ROOT, capture_output=True, text=True, check=True,
        )
        prefix = ("MATCHED " if expected else "NOT MATCHED ") + RULE + " "
        assert any(line.startswith(prefix) for line in result.stdout.splitlines()), result.stdout
        print(name + ": passed", flush=True)
