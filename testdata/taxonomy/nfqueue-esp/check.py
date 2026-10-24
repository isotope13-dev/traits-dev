#!/usr/bin/env python3
"""Verify language variants, each missing role, and benign controls."""
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
CASES = json.loads(Path(__file__).with_name("cases.json").read_text())


def reports(source):
    decoder = json.JSONDecoder()
    while source.strip():
        source = source.lstrip()
        report, end = decoder.raw_decode(source)
        yield from report["files"]
        source = source[end:]


def main():
    result = subprocess.run(
        [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
         "--disable", "third-party,radare2,upx", "--format", "json", "analyze",
         *[str(ROOT / case["file"]) for case in CASES]],
        check=True, capture_output=True, text=True, cwd=ROOT,
    )
    files = {str(Path(f["path"]).resolve()): f for f in reports(result.stdout)}
    for case in CASES:
        report = files[str(ROOT / case["file"])]
        ids = {trait["id"] for trait in report.get("traits", [])}
        missing = set(case["matched"]) - ids
        unexpected = set(case["not_matched"]) & ids
        assert not missing and not unexpected, (case["file"], missing, unexpected)
        print("PASS", case["file"])


if __name__ == "__main__":
    main()
