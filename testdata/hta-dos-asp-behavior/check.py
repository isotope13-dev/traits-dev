#!/usr/bin/env python3
"""Check behavior boundaries without executing fixture code."""
import json
import os
from pathlib import Path
import subprocess


root = Path(__file__).resolve().parents[2]
cases = json.loads(Path(__file__).with_name("cases.json").read_text())["fixtures"]
command = [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(root),
           "--format", "json"] + [str(root / case["path"]) for case in cases]
result = subprocess.run(command, cwd=root, text=True, capture_output=True,
                        env={**os.environ, "CLEAVE_VALIDATE": "0"}, check=True)
decoder = json.JSONDecoder()
remaining = result.stdout
files = {}
while remaining.strip():
    document, end = decoder.raw_decode(remaining.lstrip())
    remaining = remaining.lstrip()[end:]
    for file in document["files"]:
        files[str(Path(file["path"]).resolve())] = file
for case in cases:
    file = files[str((root / case["path"]).resolve())]
    ids = {trait["id"] for trait in file.get("traits", [])}
    missing = set(case["matched"]) - ids
    unexpected = set(case["not_matched"]) & ids
    assert not missing and not unexpected, (case["path"], missing, unexpected)
print(f"PASS: {len(cases)} positive and near-miss fixtures")
