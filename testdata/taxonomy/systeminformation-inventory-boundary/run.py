#!/usr/bin/env python3
"""Check inventory placement, retained capabilities and nearby false positives."""
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
cases = json.loads((HERE / "cases.json").read_text())
result = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
     "--format", "json", *[str(HERE / case["path"]) for case in cases["fixtures"]]],
    text=True, capture_output=True, check=True,
)
decoder = json.JSONDecoder()
remaining = result.stdout.lstrip()
files = {}
while remaining:
    report, end = decoder.raw_decode(remaining)
    files.update({Path(f["path"]).name: f for f in report["files"]})
    remaining = remaining[end:].lstrip()
retired = set(cases["id_map"]) | set(cases["retired"])
for case in cases["fixtures"]:
    traits = {t["id"]: t for t in files[case["path"]].get("traits", [])}
    missing = set(case.get("required", [])) - traits.keys()
    unwanted = (set(case.get("forbidden", [])) | retired) & traits.keys()
    assert not missing, (case["path"], "missing", sorted(missing))
    assert not unwanted, (case["path"], "unexpected", sorted(unwanted))
    for trait in case.get("required", []):
        expected = case.get("expected_criticalities", {}).get(trait, 3)
        assert traits[trait]["crit"] == expected, (case["path"], trait)
    print(case["path"], "PASS")
