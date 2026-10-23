#!/usr/bin/env python3
"""Static source-binding controls; never execute the specimen code."""
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CASES = json.loads((HERE / "cases.json").read_text())
TRAITS = ["objectives/exfiltration/stealer/system-info/network::" + suffix
          for suffix in ("hex-table-axios-mac-inventory-post", "js-concealed-mac-inventory-post")]
run = subprocess.run([os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT), "--json"]
                     + [str(HERE / case["path"]) for case in CASES],
                     capture_output=True, text=True)
assert run.returncode in (0, 1), run.stderr
assert not run.stderr.strip(), run.stderr
reports = {}
for line in run.stdout.splitlines():
    for file in json.loads(line)["files"]:
        reports[Path(file["path"]).name] = {t["id"] for t in file.get("traits", [])}
for case in CASES:
    for trait in TRAITS:
        expected = case.get("hostile", case["present"]) if trait == TRAITS[1] else case["present"]
        assert (trait in reports[case["file"]]) == expected, (case["file"], trait)
print(f"{len(CASES) * len(TRAITS)} assertions passed across {len(CASES)} static fixtures")
