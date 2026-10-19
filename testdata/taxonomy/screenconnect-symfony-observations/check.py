#!/usr/bin/env python3
"""Run focused controls from the repository root; never executes fixtures."""
import json
import os
from pathlib import Path
import subprocess

base = Path(__file__).resolve().parent
repo = base.parents[2]
cases = json.loads((base / "cases.json").read_text())
engine = os.environ.get("CLEAVE", "cleave")
failures = []
for case in cases["fixtures"]:
    result = subprocess.run([engine, "--traits-dir", str(repo), "--json", case["path"]],
                            cwd=repo, text=True, capture_output=True, check=True)
    report = json.loads(result.stdout)
    traits = {trait["id"] for file in report["files"] for trait in file.get("traits", [])}
    missing = set(case["matched"]) - traits
    unwanted = set(case["not_matched"]) & traits
    if missing or unwanted:
        failures.append((case["case_id"], sorted(missing), sorted(unwanted)))
for case in cases["text_controls"]:
    result = subprocess.run([engine, "--traits-dir", str(repo), "test-match",
                             str(base / case["file"]), "--type", "text",
                             "--method", case["method"], "--pattern", case["pattern"]],
                            cwd=repo, text=True, capture_output=True, check=True)
    matched = "MATCHED (" in result.stdout
    if matched != case["matched"]:
        failures.append((case["file"], case["pattern"], result.stdout))
if failures:
    raise SystemExit(json.dumps(failures, indent=2))
print(f"PASS: {len(cases['fixtures'])} scan controls and {len(cases['text_controls'])} text controls")
