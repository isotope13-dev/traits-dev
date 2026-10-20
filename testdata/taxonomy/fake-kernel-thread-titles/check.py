#!/usr/bin/env python3
"""Check call binding, near misses, and reconstructed cron-persistent variants."""
import json
import os
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[3]
cases = json.loads(Path(__file__).with_name("cases.json").read_text())["fixtures"]
result = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(root),
     "--format", "json", "analyze", *[case["path"] for case in cases]],
    text=True, capture_output=True, check=True,
)
decoder = json.JSONDecoder()
remaining = result.stdout.lstrip()
reports = {}
while remaining:
    report, end = decoder.raw_decode(remaining)
    remaining = remaining[end:].lstrip()
    for file in report["files"]:
        reports[file["path"]] = {trait["id"] for trait in file.get("traits", [])}

for case in cases:
    matched = reports[case["path"]]
    missing = set(case["matched"]) - matched
    unexpected = set(case["not_matched"]) & matched
    assert not missing and not unexpected, (case["case_id"], missing, unexpected)
print(f"PASS: {len(cases)} focused cases")
