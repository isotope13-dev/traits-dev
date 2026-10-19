"""Check intentional obfuscation controls without assigning them a benign label."""
import json
import os
from pathlib import Path
import subprocess

base = Path(__file__).resolve().parent
repo = base.parents[2]
cases = json.loads((base / "cases.json").read_text())
result = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(repo),
     "--format", "json", *[str(repo / case["path"]) for case in cases]],
    check=False, capture_output=True, text=True,
)
if result.returncode:
    raise RuntimeError(result.stderr)
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
    traits = file.get("traits", [])
    ids = {trait["id"] for trait in traits}
    assert set(case.get("required", [])).issubset(ids), case["path"]
    assert not set(case.get("forbidden", [])).intersection(ids), case["path"]
    hostile = sum(trait["crit"] == 5 for trait in traits)
    suspicious = sum(trait["crit"] == 4 for trait in traits)
    assert hostile >= case.get("min_hostile", 0), case["path"]
    assert hostile <= case.get("max_hostile", hostile), case["path"]
    assert suspicious == case.get("suspicious", suspicious), case["path"]
print(f"OSA Mach-O controls: {len(cases)}/{len(cases)} passed")
