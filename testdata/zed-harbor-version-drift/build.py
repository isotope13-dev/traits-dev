#!/usr/bin/env python3
"""Rebuild inert native controls on macOS; never execute them."""
import os
from pathlib import Path
import subprocess

root = Path(__file__).parent
for source in sorted(root.glob("*.c")):
    subprocess.run(["cc", "-O0", str(source), "-o", str(source.with_suffix(".macho"))], check=True)
env = dict(os.environ, GOOS="darwin", GOARCH="arm64", CGO_ENABLED="0")
subprocess.run(["go", "build", "-trimpath", "-o", str(root / "system-info-go.macho"), str(root / "system-info.go")], env=env, check=True)
