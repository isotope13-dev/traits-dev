#!/usr/bin/env python3
"""Check source-call false positives, decoder coverage, and retained consumers."""
import json
import os
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[3]
cases = json.loads(Path(__file__).with_name("cases.json").read_text())
result = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(root),
     "--format", "json", *[str(root / case["path"]) for case in cases]],
    text=True, capture_output=True, check=True,
)
# The CLI's multi-target JSON stream may concatenate objects without newlines.
data = result.stdout
decoder = json.JSONDecoder()
files = {}
while data.strip():
    data = data.lstrip()
    report, length = decoder.raw_decode(data)
    data = data[length:]
    for file in report["files"]:
        files[str(Path(file["path"]).resolve())] = file
for case in cases:
    file = files[str((root / case["path"]).resolve())]
    traits = {trait["id"]: trait for trait in file.get("traits", [])}
    assert set(case.get("required", [])) <= traits.keys(), (case["path"], "missing", set(case.get("required", [])) - traits.keys())
    assert not set(case.get("forbidden", [])) & traits.keys(), (case["path"], "forbidden")
    if case.get("max_alerts") is not None:
        assert sum(t["crit"] >= 4 for t in traits.values()) <= case["max_alerts"], case["path"]
print(f"PASS: {len(cases)} controls; attack coverage and benign near misses preserved")
