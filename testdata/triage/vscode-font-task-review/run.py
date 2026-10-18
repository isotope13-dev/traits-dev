#!/usr/bin/env python3
"""Check task scoping, neutral lookup placement, and disguised autorun."""
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
cases = json.loads((HERE / "cases.json").read_text())
result = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
     "--format", "json", *[str(HERE / name) for name in cases]],
    capture_output=True, text=True,
)
if result.returncode:
    raise SystemExit(result.stderr)
decoder = json.JSONDecoder()
pending = result.stdout.lstrip()
files = {}
while pending:
    report, end = decoder.raw_decode(pending)
    for item in report["files"]:
        files[Path(item["path"]).name] = item
    pending = pending[end:].lstrip()

checks = 0
for name, expected in cases.items():
    actual = {item["id"] for item in files[name]["traits"]}
    for trait, present in expected.items():
        assert (trait in actual) == present, (name, trait, present)
        checks += 1
    if name.endswith(("ordinary-lint.json", "font-build.json")):
        assert not any(t["crit"] == 5 for t in files[name]["traits"]), name
        assert sum(t["crit"] == 4 for t in files[name]["traits"]) <= 1, name
print(f"PASS: {checks} trait assertions across {len(cases)} fixtures")
