#!/usr/bin/env python3
"""Check static findings only; never run the fixture programs."""
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
cases = json.loads((HERE / "cases.json").read_text())
result = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
     "--format", "json", *[str(HERE / case["file"]) for case in cases]],
    capture_output=True, text=True, check=True)
assert not result.stderr.strip(), result.stderr
reports = result.stdout
found = {}
while reports.strip():
    report, end = json.JSONDecoder().raw_decode(reports.lstrip())
    reports = reports.lstrip()[end:]
    for item in report["files"]:
        found[Path(item["path"]).name] = {t["id"] for t in item.get("traits", [])}
for case in cases:
    ids = found[case["file"]]
    assert set(case["present"]) <= ids, (case["file"], "missing", ids)
    assert not set(case["absent"]) & ids, (case["file"], "unexpected", ids)
print(f"{len(cases)} static placement/query controls passed")
