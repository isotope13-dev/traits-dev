#!/usr/bin/env python3
"""Generate a Cargo .crate (gzipped tar with a name-version prefix directory)."""

from __future__ import annotations

import io
import sys
import tarfile
import time
from pathlib import Path

NAME = "sample"
VERSION = "0.1.0"
PREFIX = f"{NAME}-{VERSION}"

CARGO_TOML = """[package]
name = "sample"
version = "0.1.0"
edition = "2021"
license = "MIT"
description = "A sample crate that does nothing."
"""

LIB_RS = """//! A sample crate.

pub fn message() -> &'static str {
    "this sample does nothing"
}
"""

VCS_INFO = """{"git":{"sha1":"0000000000000000000000000000000000000000"}}
"""


def add(tar: tarfile.TarFile, name: str, data: str) -> None:
    payload = data.encode("utf-8")
    info = tarfile.TarInfo(name=f"{PREFIX}/{name}")
    info.size = len(payload)
    info.mtime = int(time.time())
    info.mode = 0o644
    tar.addfile(info, io.BytesIO(payload))


def main(target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(target, "w:gz") as tar:
        add(tar, "Cargo.toml", CARGO_TOML)
        add(tar, "src/lib.rs", LIB_RS)
        add(tar, ".cargo_vcs_info.json", VCS_INFO)


if __name__ == "__main__":
    main(Path(sys.argv[1]))
