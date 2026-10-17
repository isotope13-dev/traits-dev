#!/usr/bin/env python3
"""Check source-to-send and download-to-launch identifier relationships."""
import json
import subprocess
from pathlib import Path

cases = json.loads(Path(__file__).with_name("cases.json").read_text())["fixtures"]
result = subprocess.run(
    ["cleave", "--traits-dir", ".", "--format", "json"] + [c["path"] for c in cases],
    check=True, capture_output=True, text=True,
)
reports = {}
pending = result.stdout.lstrip()
decoder = json.JSONDecoder()
while pending:
    report, end = decoder.raw_decode(pending)
    pending = pending[end:].lstrip()
    for f in report["files"]:
        reports[str(Path(f["path"]).resolve())] = {t["id"] for t in f.get("traits", [])}
failures = []
for case in cases:
    actual = reports[str(Path(case["path"]).resolve())]
    for trait in case["matched"]:
        if trait not in actual:
            failures.append(f"{case['path']}: missing {trait}")
    for trait in case["not_matched"]:
        if trait in actual:
            failures.append(f"{case['path']}: unexpected {trait}")
assert not failures, "\n".join(failures)
print(f"PASS: {len(cases)} relationship and near-miss fixtures")
