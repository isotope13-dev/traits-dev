#!/usr/bin/env python3
"""Check source-concealment coverage without executing any fixture."""
import json
import os
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[3]
cases = json.loads(Path(__file__).with_name("cases.json").read_text())
for case in cases["fixtures"]:
    result = subprocess.run(
        [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(root),
         "--format", "json", str(root / case["path"])],
        check=True, capture_output=True, text=True,
    )
    traits = json.loads(result.stdout)["files"][0]["traits"]
    observed = {trait["id"]: trait["crit"] for trait in traits}
    for trait_id, severity in case["required"].items():
        assert observed.get(trait_id) == severity, (case["path"], trait_id)
    assert not set(case["forbidden"]) & observed.keys(), case["path"]
    assert not set(cases["id_map"]) & observed.keys(), case["path"]
    assert sum(t["crit"] == 5 for t in traits) == case["hostile"], case["path"]
    assert sum(t["crit"] == 4 for t in traits) == case["suspicious"], case["path"]
    print("PASS", case["path"])
