#!/usr/bin/env python3
"""Check device-path precision and generic Go writer placement."""
import json
from pathlib import Path
import subprocess

cases = Path(__file__).with_name("cases.json")
for case in json.loads(cases.read_text())["fixtures"]:
    result = subprocess.run(
        ["cleave", "--traits-dir", ".", "--format", "json", case["path"]],
        check=True, capture_output=True, text=True,
    )
    report = json.loads(result.stdout)
    traits = {t["id"] for f in report["files"] for t in f.get("traits", [])}
    missing = set(case["matched"]) - traits
    unexpected = set(case["not_matched"]) & traits
    assert not (missing or unexpected), (case["path"], missing, unexpected)
    print("PASS", case["path"])
