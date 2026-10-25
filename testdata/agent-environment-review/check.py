#!/usr/bin/env python3
"""Scan inert agent recipes and check behavior boundaries without executing them."""
import json
import os
from pathlib import Path
import subprocess

here = Path(__file__).resolve().parent
root = here.parents[1]
cases = json.loads((here / "cases.json").read_text())
paths = [here / c["file"] for c in cases]
r = subprocess.run([os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(root),
                    "--format", "json", *map(str, paths)],
                   capture_output=True, text=True)
if r.returncode:
    raise SystemExit(r.stderr)
remaining = r.stdout
decoder = json.JSONDecoder()
files = {}
while remaining.strip():
    remaining = remaining.lstrip()
    report, end = decoder.raw_decode(remaining)
    remaining = remaining[end:]
    for entry in report["files"]:
        files[str(Path(entry["path"]).resolve())] = entry
for case, path in zip(cases, paths):
    traits = {t["id"]: t["crit"] for t in files[str(path)]["traits"]}
    for trait, crit in case.get("required", {}).items():
        assert traits.get(trait) == crit, (case["file"], trait, traits.get(trait), crit)
    assert not set(case.get("forbidden", [])) & traits.keys(), case["file"]
    if "max_crit" in case:
        assert all(c <= case["max_crit"] for c in traits.values()), (case["file"], traits)
print(f"{len(cases)} agent environment behavior controls passed")
