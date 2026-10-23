#!/usr/bin/env python3
"""Analyze controls as data; never execute specimen code."""
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
cases = json.loads((HERE / "cases.json").read_text())
result = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
     "--format", "jsonl", *[str(ROOT / name) for name in cases]],
    check=True, capture_output=True, text=True,
)
observed = {
    Path(file["path"]).name: {trait["id"] for trait in file.get("traits", [])}
    for line in result.stdout.splitlines() if line.strip()
    for file in json.loads(line)["files"]
}
for path, expectation in cases.items():
    actual = observed[Path(path).name]
    missing = set(expectation["required"]) - actual
    unexpected = set(expectation["forbidden"]) & actual
    assert not missing and not unexpected, (path, missing, unexpected)
print(f"Passed {len(cases)} static source and attack controls")
