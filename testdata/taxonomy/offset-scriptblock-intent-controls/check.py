#!/usr/bin/env python3
"""Static regression checks. Never execute the PowerShell fixture source."""
import json
import os
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[3]
cases = json.loads(Path(__file__).with_name("cases.json").read_text())
for fixture in cases["fixtures"]:
    result = subprocess.run(
        [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(root),
         "--format", "json", str(root / fixture["path"])],
        check=True, capture_output=True, text=True,
    )
    report = json.loads(result.stdout)
    traits = report["files"][0]["traits"]
    by_id = {trait["id"]: trait for trait in traits}
    assert set(fixture["matched"]) <= by_id.keys(), fixture["path"]
    assert not set(fixture["not_matched"]) & by_id.keys(), fixture["path"]
    assert not any(t["crit"] == 5 for t in traits), fixture["path"]
    expected_suspicious = 1 if "offset-hello" in fixture["path"] else 0
    assert sum(t["crit"] == 4 for t in traits) == expected_suspicious
    print("PASS", fixture["path"])
