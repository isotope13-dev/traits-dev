#!/usr/bin/env python3
"""Run static-analysis controls; never execute fixture payloads."""
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
cases = json.loads((HERE / "cases.json").read_text())["cases"]
result = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
     "--format", "json", *[str(ROOT / c["path"]) for c in cases]],
    capture_output=True, text=True, check=True,
)
decoder = json.JSONDecoder()
remaining = result.stdout
files = {}
while remaining.strip():
    report, consumed = decoder.raw_decode(remaining.lstrip())
    remaining = remaining.lstrip()[consumed:]
    for artifact in report.get("files", []):
        files[str(Path(artifact["path"]).resolve())] = artifact
errors = []
for case in cases:
    artifact = files.get(str((ROOT / case["path"]).resolve()))
    if artifact is None:
        errors.append("missing report: " + case["path"])
        continue
    traits = {t["id"] for t in artifact.get("traits", [])}
    errors.extend(case["path"] + ": missing " + t
                  for t in case["required"] if t not in traits)
    errors.extend(case["path"] + ": unexpected " + t
                  for t in case["forbidden"] if t in traits)
if errors:
    raise SystemExit("\n".join(errors))
print(str(len(cases)) + " focused controls passed")
