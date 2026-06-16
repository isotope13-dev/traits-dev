#!/usr/bin/env python3
"""Build minimal tar-based package fixtures."""

from __future__ import annotations

import io
import sys
import tarfile
from pathlib import Path

MESSAGE = b"this sample does nothing\n"

ALPINE_PKGINFO = b"""pkgname = sample
pkgver = 0.1.0-r0
arch = noarch
pkgdesc = sample package that does nothing
"""

ARCH_PKGINFO = b"""pkgname = sample
pkgver = 0.1.0-1
pkgdesc = sample package that does nothing
arch = any
"""

FREEBSD_MANIFEST = b"""{
  "name": "sample",
  "version": "0.1.0",
  "origin": "local/sample",
  "comment": "sample package that does nothing"
}
"""


def add_bytes(tar: tarfile.TarFile, name: str, data: bytes, mode: int = 0o644) -> None:
    info = tarfile.TarInfo(name)
    info.size = len(data)
    info.mode = mode
    info.mtime = 0
    tar.addfile(info, io.BytesIO(data))


def build_tar(target: Path, entries: list[tuple[str, bytes]]) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(target, "w") as tar:
        for name, data in entries:
            add_bytes(tar, name, data)


def build_tgz(target: Path, entries: list[tuple[str, bytes]]) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(target, "w:gz") as tar:
        for name, data in entries:
            add_bytes(tar, name, data)


def main(kind: str, target: Path) -> None:
    if kind == "alpine":
        build_tgz(
            target,
            [
                (".PKGINFO", ALPINE_PKGINFO),
                ("usr/share/doc/sample/README", MESSAGE),
            ],
        )
    elif kind == "arch":
        build_tar(
            target,
            [
                (".PKGINFO", ARCH_PKGINFO),
                ("usr/share/doc/sample/README", MESSAGE),
            ],
        )
    elif kind == "freebsd":
        build_tar(
            target,
            [
                ("+MANIFEST", FREEBSD_MANIFEST),
                ("usr/local/share/doc/sample/README", MESSAGE),
            ],
        )
    else:
        raise SystemExit(f"unknown kind: {kind}")


if __name__ == "__main__":
    main(sys.argv[1], Path(sys.argv[2]))
