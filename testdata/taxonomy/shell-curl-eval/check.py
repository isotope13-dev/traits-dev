#!/usr/bin/env python3
"""Check deployment, syntax near misses, relocations and retained consumers."""
import json
import os
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[3]
fixture_dir = Path(__file__).resolve().parent
run = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(root),
     "--format", "json", str(fixture_dir),
     str(root / "testdata/hostile/registry-hook-propagation.sh")],
    check=True, capture_output=True, text=True,
)
remaining = run.stdout
results = {}
decoder = json.JSONDecoder()
while remaining.strip():
    remaining = remaining.lstrip()
    report, end = decoder.raw_decode(remaining)
    remaining = remaining[end:]
    for file in report.get("files", []):
        results[Path(file["path"]).name] = {
            trait["id"]: trait["crit"] for trait in file.get("traits", [])
        }
cases = json.loads((fixture_dir / "cases.json").read_text())["fixtures"]
for case in cases:
    name = Path(case["path"]).name
    assert name in results, f"No report for {name}"
    found = results[name]
    missing = set(case["matched"]) - found.keys()
    unexpected = set(case["not_matched"]) & found.keys()
    assert not (missing or unexpected), (name, missing, unexpected)
for local_id in ["aur-install-script-poisoning-push", "npm-credential-fanout-hook-propagation"]:
    full_id = "objectives/supply-chain/hidden-payload/worm::" + local_id
    assert results["registry-hook-propagation.sh"].get(full_id) == 5, full_id
print(f"Passed {len(cases)} controls and retained both propagation convictions")
