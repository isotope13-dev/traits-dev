#!/usr/bin/env python3
"""Scan original bytes, re-encoded variants and benign near misses; never execute."""
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
cases = json.loads((HERE / "cases.json").read_text())
command = [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT), "--json"]
result = subprocess.run(command + [str(HERE / c["file"]) for c in cases],
                        check=True, capture_output=True, text=True)
reports = [json.loads(line) for line in result.stdout.splitlines() if line.strip()]
files = {Path(f["path"]).name: f for r in reports for f in r["files"]}
errors = []
for case in cases:
    name = case["file"]
    traits = {t["id"] for t in files[name].get("traits", [])}
    errors += [f"{name}: missing {t}" for t in case["required"] if t not in traits]
    errors += [f"{name}: unexpected {t}" for t in case["forbidden"] if t in traits]
    errors += [f"{name}: unexpected hostile {t['id']}"
               for t in files[name].get("traits", []) if t["crit"] == 5]
if errors:
    raise SystemExit("\n".join(errors))
print(f"Passed {len(cases)} original, variant and near-miss controls")
