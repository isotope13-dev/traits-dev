#!/usr/bin/env python3
"""Check reconstruction boundaries and preserve SVG capability consumers."""
import json
import os
from pathlib import Path
import subprocess

folder = Path(__file__).resolve().parent
root = folder.parents[2]
cases = json.loads((folder / "cases.json").read_text())
engine = os.environ.get("CLEAVE", "cleave")
command = [engine, "--traits-dir", str(root), "--format", "jsonl"]
command.extend(str((folder / name).resolve()) for name in cases)
result = subprocess.run(command, check=True, capture_output=True, text=True)
reports = [json.loads(line) for line in result.stdout.splitlines() if line.strip()]
findings = {
    str(Path(file["path"]).resolve()): {trait["id"] for trait in file.get("traits", [])}
    for report in reports
    for file in report["files"]
}
checks = 0
for name, expected in cases.items():
    observed = findings[str((folder / name).resolve())]
    for trait, present in expected.items():
        assert (trait in observed) == present, (name, trait, present)
        checks += 1
print(f"Passed {checks} assertions across {len(cases)} controls")
