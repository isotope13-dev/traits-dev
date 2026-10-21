"""Static-only compiled AppleScript detection controls; execute no specimen."""
import json
import os
from pathlib import Path
import subprocess

base = Path(__file__).resolve().parent
repo = base.parents[2]
cases = json.loads((base / "cases.json").read_text())
result = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(repo),
     "--json", *[str(repo / case["path"]) for case in cases]],
    capture_output=True, text=True, check=True,
)
decoder = json.JSONDecoder()
remaining = result.stdout
files = {}
while remaining.strip():
    report, end = decoder.raw_decode(remaining.lstrip())
    remaining = remaining.lstrip()[end:]
    for file in report.get("files", [report]):
        files[file["path"]] = file
for case in cases:
    file = files[str(repo / case["path"])]
    traits = {trait["id"]: trait for trait in file.get("traits", [])}
    assert set(case.get("required", [])).issubset(traits), (case["path"], "missing", set(case.get("required", [])) - traits.keys())
    assert not set(case.get("forbidden", [])).intersection(traits), (case["path"], "forbidden")
    for trait_id, criticality in case.get("criticalities", {}).items():
        assert traits[trait_id]["crit"] == criticality, (case["path"], trait_id)
    hostile = sum(trait["crit"] == 5 for trait in traits.values())
    assert hostile <= case.get("max_hostile", hostile), (case["path"], hostile)
print(f"Compiled AppleScript second review: {len(cases)}/{len(cases)} passed")
