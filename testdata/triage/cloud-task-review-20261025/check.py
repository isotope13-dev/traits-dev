#!/usr/bin/env python3
"""Check source relationships and retained cloud-task coverage without execution."""
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
cases = json.loads((HERE / "cases.json").read_text())["fixtures"]
output = subprocess.check_output(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
     "--format", "json", "analyze", *[case["path"] for case in cases]],
    cwd=ROOT, text=True,
)
decoder = json.JSONDecoder()
files = {}
while output.strip():
    report, end = decoder.raw_decode(output.lstrip())
    output = output.lstrip()[end:]
    files.update({file["path"]: file for file in report["files"]})

for case in cases:
    file = files[case["path"]]
    traits = {trait["id"]: trait for trait in file["traits"]}
    missing = set(case["matched"]) - traits.keys()
    unexpected = set(case["not_matched"]) & traits.keys()
    assert not missing and not unexpected, (case["path"], missing, unexpected)
    if "hostile_count" in case:
        hostile = sum(trait["crit"] == 5 for trait in traits.values())
        assert hostile == case["hostile_count"], (case["path"], hostile)
print(f"Passed {len(cases)} cloud-task relationship and retention cases")
