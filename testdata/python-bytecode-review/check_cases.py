#!/usr/bin/env python3
"""Run from the repository root; never executes the source fixtures."""
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
cases = json.loads((HERE / "cases.json").read_text())
result = subprocess.run(
    ["cleave", "--traits-dir", ".", "--format", "jsonl", str(HERE)],
    check=True, text=True, capture_output=True,
)
observed = {}
for line in result.stdout.splitlines():
    for file in json.loads(line).get("files", []):
        observed[Path(file["path"]).name] = {t["id"] for t in file.get("traits", [])}
for name, case in cases.items():
    found = observed[name]
    assert set(case.get("matched", [])) <= found, (name, "missing", set(case.get("matched", [])) - found)
    assert not (set(case.get("not_matched", [])) & found), (name, "unexpected", set(case.get("not_matched", [])) & found)
print(f"Passed {len(cases)} behavioral controls")
