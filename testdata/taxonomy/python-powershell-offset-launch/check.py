#!/usr/bin/env python3
"""Check static source binding; never execute fixture PowerShell."""
import json
import os
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[3]
cases = json.loads(Path(__file__).with_name("cases.json").read_text())["fixtures"]
result = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(root),
     "--format", "json", *(str(root / case["path"]) for case in cases)],
    check=True, capture_output=True, text=True,
)
decoder = json.JSONDecoder()
remaining = result.stdout.strip()
reports = {}
while remaining:
    report, end = decoder.raw_decode(remaining)
    reports.update({Path(item["path"]).resolve(): item
                    for item in report["files"]})
    remaining = remaining[end:].lstrip()
for case in cases:
    report = reports[(root / case["path"]).resolve()]
    ids = {trait["id"] for trait in report["traits"]}
    assert set(case["matched"]) <= ids, case["path"]
    assert not set(case["not_matched"]) & ids, case["path"]
    assert not any(trait["crit"] == 5 for trait in report["traits"])
    print("PASS", case["path"])
