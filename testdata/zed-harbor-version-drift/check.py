#!/usr/bin/env python3
"""Check the native trait boundaries without executing any fixture."""
import json
from pathlib import Path
import subprocess

cases = json.loads(Path(__file__).with_name("cases.json").read_text())
for fixture in cases["fixtures"]:
    ids = fixture.get("matched", []) + fixture.get("not_matched", [])
    run = subprocess.run(["cleave", "--traits-dir", ".", "test-rules", fixture["path"], "--rules", ",".join(ids)], text=True, capture_output=True, check=True)
    matched = {line.split()[1] for line in run.stdout.splitlines() if line.startswith("MATCHED ")}
    for rule in fixture.get("matched", []):
        assert rule in matched, (fixture["path"], rule, run.stdout)
    for rule in fixture.get("not_matched", []):
        assert rule not in matched, (fixture["path"], rule, run.stdout)
    print("PASS", fixture["path"])
