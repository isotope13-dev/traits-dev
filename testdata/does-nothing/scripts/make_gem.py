#!/usr/bin/env python3
"""Generate a minimal RubyGem (.gem).

A .gem is a POSIX tar containing three members:
  - metadata.gz    (YAML gemspec, gzipped)
  - data.tar.gz    (the gem's files)
  - checksums.yaml.gz (optional)

We emit metadata.gz and data.tar.gz; that is enough for type detectors.
"""

from __future__ import annotations

import gzip
import io
import sys
import tarfile
import time
from pathlib import Path

METADATA_YAML = """--- !ruby/object:Gem::Specification
name: sample
version: !ruby/object:Gem::Version
  version: 0.1.0
platform: ruby
authors:
  - example
date: 2026-01-01 00:00:00.000000000 Z
summary: A sample gem that does nothing.
description: A sample gem that does nothing.
email: []
executables: []
extensions: []
require_paths:
  - lib
rubygems_version: 3.5.0
specification_version: 4
"""

LIB_RB = """# frozen_string_literal: true

module Sample
  MESSAGE = "this sample does nothing"
end
"""


def tar_member(tar: tarfile.TarFile, name: str, data: bytes, mode: int = 0o644) -> None:
    info = tarfile.TarInfo(name=name)
    info.size = len(data)
    info.mtime = int(time.time())
    info.mode = mode
    tar.addfile(info, io.BytesIO(data))


def main(target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)

    data_buf = io.BytesIO()
    with tarfile.open(fileobj=data_buf, mode="w:gz") as inner:
        tar_member(inner, "lib/sample.rb", LIB_RB.encode("utf-8"))
    data_tar_gz = data_buf.getvalue()

    metadata_gz = gzip.compress(METADATA_YAML.encode("utf-8"))

    with tarfile.open(target, "w") as outer:
        tar_member(outer, "metadata.gz", metadata_gz)
        tar_member(outer, "data.tar.gz", data_tar_gz)


if __name__ == "__main__":
    main(Path(sys.argv[1]))
