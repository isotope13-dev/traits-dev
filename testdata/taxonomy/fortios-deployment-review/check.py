"""Scan fixtures as data; never execute their deployment commands."""
import json
import os
from pathlib import Path
import subprocess


directory = Path(__file__).resolve().parent
root = directory.parents[2]
cases = json.loads((directory / "cases.json").read_text())["fixtures"]
result = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(root),
     "--format", "json", *[str(directory / case["path"]) for case in cases]],
    check=True, capture_output=True, text=True,
)
decoder = json.JSONDecoder()
remaining = result.stdout.strip()
reports = {}
while remaining:
    report, end = decoder.raw_decode(remaining)
    for file in report["files"]:
        reports[Path(file["path"]).name] = file
    remaining = remaining[end:].lstrip()

for case in cases:
    file = reports[case["path"]]
    traits = {trait["id"]: trait["crit"] for trait in file.get("traits", [])}
    for trait, criticality in case["expected"].items():
        assert traits.get(trait) == criticality, (case["path"], trait, traits.get(trait))
    for trait in case["absent"]:
        assert trait not in traits, (case["path"], trait)
    assert max(traits.values(), default=0) <= case["max_criticality"], case["path"]

print(f"PASS: {len(cases)} FortiOS and SSH positive/negative controls")
