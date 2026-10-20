#!/usr/bin/env python3
"""Focused controls for source concealment, wallet hooks, and neutral moves."""
import json
import os
from pathlib import Path
import subprocess
import shutil
import tempfile
from fixtures import pe

root = Path(__file__).resolve().parents[2]
cases = json.loads(Path(__file__).with_name("cases.json").read_text())
# Test-directory exclusions must not supply the benign context being tested.
with tempfile.TemporaryDirectory(prefix="review-controls-", dir=root) as temp:
    copies = []
    for case in cases:
        copy = Path(temp) / Path(case["path"]).name
        if "generated_pe" in case:
            variant = case["generated_pe"]
            copy.write_bytes(pe(
                0 if variant == "peb-small" else 524288,
                peb=variant != "overlay-no-peb",
                truncated=variant == "peb-truncated-cert",
            ))
        elif "generated_text" in case:
            text = case["generated_text"]
            copy.write_text(text["prefix"] + text["repeat"] * text["count"] + text["suffix"])
        else:
            shutil.copyfile(root / case["path"], copy)
        copies.append(str(copy))
    result = subprocess.run(
        [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(root),
         "--format", "json", *copies],
        check=True, capture_output=True, text=True,
    )
decoder = json.JSONDecoder()
remaining = result.stdout.lstrip()
files = {}
while remaining:
    report, end = decoder.raw_decode(remaining)
    files.update({Path(f["path"]).name: f for f in report["files"]})
    remaining = remaining[end:].lstrip()
for case in cases:
    file = files[Path(case["path"]).name]
    ids = {t["id"] for t in file.get("traits", [])}
    missing = set(case["required"]) - ids
    extra = set(case["forbidden"]) & ids
    assert not missing and not extra, (case["path"], missing, extra)
    print("PASS", Path(case["path"]).name)
