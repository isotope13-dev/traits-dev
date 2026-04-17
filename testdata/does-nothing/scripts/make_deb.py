#!/usr/bin/env python3
"""Build a minimal Debian package (.deb).

A .deb is a Unix `ar` archive containing three members in order:
  1. debian-binary  (text "2.0\n")
  2. control.tar.gz (package metadata: control, md5sums, ...)
  3. data.tar.gz    (package payload rooted at /)
"""

from __future__ import annotations

import io
import sys
import tarfile
import time
from pathlib import Path

CONTROL = """Package: sample
Version: 0.1.0
Architecture: all
Maintainer: example <example@example.com>
Description: A sample package that does nothing.
Section: misc
Priority: optional
"""

MESSAGE = "this sample does nothing\n"


def tar_member(tar: tarfile.TarFile, name: str, data: bytes, mode: int = 0o644) -> None:
    info = tarfile.TarInfo(name=name)
    info.size = len(data)
    info.mtime = int(time.time())
    info.mode = mode
    tar.addfile(info, io.BytesIO(data))


def ar_header(name: str, size: int) -> bytes:
    return (
        f"{name:<16}{int(time.time()):<12}0     0     100644  {size:<10}`\n"
    ).encode("ascii")


def ar_append(out: io.BytesIO, name: str, data: bytes) -> None:
    out.write(ar_header(name, len(data)))
    out.write(data)
    if len(data) % 2 == 1:
        out.write(b"\n")


def main(target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)

    control_buf = io.BytesIO()
    with tarfile.open(fileobj=control_buf, mode="w:gz") as tar:
        tar_member(tar, "./control", CONTROL.encode("utf-8"))
    control_tar_gz = control_buf.getvalue()

    data_buf = io.BytesIO()
    with tarfile.open(fileobj=data_buf, mode="w:gz") as tar:
        tar_member(tar, "./usr/share/doc/sample/README", MESSAGE.encode("utf-8"))
    data_tar_gz = data_buf.getvalue()

    ar = io.BytesIO()
    ar.write(b"!<arch>\n")
    ar_append(ar, "debian-binary", b"2.0\n")
    ar_append(ar, "control.tar.gz", control_tar_gz)
    ar_append(ar, "data.tar.gz", data_tar_gz)

    target.write_bytes(ar.getvalue())


if __name__ == "__main__":
    main(Path(sys.argv[1]))
