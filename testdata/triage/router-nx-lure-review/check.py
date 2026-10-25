#!/usr/bin/env python3
"""Static regression controls; no fixture JavaScript is executed."""
import json
import os
from pathlib import Path
import subprocess

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[2]
GET = "micro-behaviors/communications/http/request/params::get-with-params"
TSX = "micro-behaviors/os/module/dynamic-load::tsimport-call"
GZIP = "micro-behaviors/data/decompress/gzip::node-create-gunzip-reference"
TAR = "micro-behaviors/data/archive/extract/tar::node-tar-extract-call"
PIPE = "micro-behaviors/data/archive/extract/tar::node-stream-to-tar-extractor"
CASES = [
    ("route-source.js", [], [GET]),
    ("get-params.js", [GET], []),
    ("get-no-params.js", [], [GET]),
    ("get-other-options.js", [], [GET]),
    ("post-params.js", [], [GET]),
    ("tsx-esm.ts", [TSX], []),
    ("tsx-cjs.js", [TSX], []),
    ("tsx-string.js", [], [TSX]),
    ("tsx-namesake.js", [], [TSX]),
    ("gzip-direct.js", [GZIP], []),
    ("gzip-compiled.js", [GZIP], []),
    ("gzip-other.js", [], [GZIP]),
    ("tar-parser.js", [TAR], []),
    ("tar-pipeline.js", [TAR, PIPE], []),
    ("tar-label.js", [], [TAR, PIPE]),
]


def main():
    result = subprocess.run(
        [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
         "--format", "json", *[str(BASE / name) for name, _, _ in CASES]],
        cwd=ROOT, capture_output=True, text=True, check=True,
    )
    decoder = json.JSONDecoder()
    reports = []
    remaining = result.stdout.lstrip()
    while remaining:
        report, end = decoder.raw_decode(remaining)
        reports.append(report)
        remaining = remaining[end:].lstrip()
    findings = {
        Path(f["path"]).name: {t["id"] for t in f.get("traits", [])}
        for report in reports for f in report["files"]
    }
    failed = False
    for name, present, absent in CASES:
        ids = findings[name]
        errors = ["missing " + x for x in present if x not in ids]
        errors += ["unexpected " + x for x in absent if x in ids]
        failed |= bool(errors)
        print(("FAIL" if errors else "PASS"), name, "; ".join(errors))
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
