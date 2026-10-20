#!/usr/bin/env python3
"""Check the configuration-reference boundary without executing fixtures."""
import json
import os
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[3]
cases = json.loads(Path(__file__).with_name("cases.json").read_text())
command = [os.environ.get("CLEAVE", "cleave"), "--no-update-check",
           "--traits-dir", str(root), "--format", "json"]
command.extend(case["path"] for case in cases["fixtures"])
result = subprocess.run(command, cwd=root, text=True, capture_output=True, check=True)
# Multiple inputs produce sequential JSON report objects.
remaining = result.stdout.strip()
reports = []
while remaining:
    report, consumed = json.JSONDecoder().raw_decode(remaining)
    reports.extend(report["files"])
    remaining = remaining[consumed:].strip()
by_path = {report["path"]: report for report in reports}
option = "micro-behaviors/os/env/provider::tailscale-derp-websocket-option"
bof = "objectives/command-and-control/channel/tunnel/tailscale::bof-derp-websocket-mesh"
for case in cases["fixtures"]:
    traits = {trait["id"]: trait for trait in by_path[case["path"]].get("traits", [])}
    assert set(case.get("matched", [])) <= traits.keys(), case["path"]
    assert not set(case.get("not_matched", [])) & traits.keys(), case["path"]
    if option in traits:
        assert traits[option]["crit"] == 3, "Option references must remain notable"
    if case["path"].endswith("bof.go"):
        assert traits[bof]["crit"] == 5, "Preserve BOF composite criticality"
    else:
        assert all(t["crit"] < 4 for t in traits.values()), case["path"]
    print("PASS", case["path"])
