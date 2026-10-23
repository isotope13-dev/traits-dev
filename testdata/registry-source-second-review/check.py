#!/usr/bin/env python3
"""Check source observations and preserved attack coverage without execution."""
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
cases = json.loads((HERE / "cases.json").read_text())["fixtures"]
paths = [str(ROOT / c["path"]) for c in cases]
run = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
     "--format", "json", *paths], check=True, capture_output=True, text=True)
remaining = run.stdout.strip()
reports = {}
decoder = json.JSONDecoder()
while remaining:
    report, end = decoder.raw_decode(remaining)
    reports.update({str(Path(f["path"]).resolve()): f for f in report["files"]})
    remaining = remaining[end:].lstrip()
for case, path in zip(cases, paths):
    traits = reports[str(Path(path).resolve())].get("traits", [])
    observed = {t["id"]: t["crit"] for t in traits}
    for trait_id, crit in case["required"].items():
        assert observed.get(trait_id) == crit, (case["path"], trait_id, observed)
    assert not set(case.get("forbidden", [])) & observed.keys(), case["path"]
    for label, severity in [("hostile", 5), ("suspicious", 4)]:
        maximum = case.get("max_" + label)
        if maximum is not None:
            assert sum(t["crit"] == severity for t in traits) <= maximum, case["path"]
    print("PASS", case["path"])
