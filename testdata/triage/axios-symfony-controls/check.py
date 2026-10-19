"""Focused matcher and migration controls; does not execute fixture code."""
import json
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parent
cases = json.loads((root / "cases.json").read_text())
result = subprocess.run(
    [sys.argv[1] if len(sys.argv) > 1 else "cleave", "--traits-dir",
     str(root.parents[2]), "--format", "json",
     *[str(root / case["file"]) for case in cases]],
    check=True, capture_output=True, text=True,
)
# Cleave emits consecutive JSON reports, including in --format json mode.
decoder = json.JSONDecoder()
remaining = result.stdout
by_path = {}
while remaining.strip():
    remaining = remaining.lstrip()
    report, end = decoder.raw_decode(remaining)
    remaining = remaining[end:]
    for unit in report["files"]:
        by_path[Path(unit["path"]).resolve()] = {
            trait["id"] for trait in unit.get("traits", [])
        }
for case in cases:
    ids = by_path[(root / case["file"]).resolve()]
    missing = set(case["present"]) - ids
    unwanted = set(case["absent"]) & ids
    assert not missing and not unwanted, (case["file"], missing, unwanted)
    print("PASS", case["file"])
