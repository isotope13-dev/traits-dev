"""Check corrected evidence placement without executing JavaScript fixtures."""
import argparse
import json
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("--cleave", default="../cleave/target/release/cleave")
parser.add_argument("--traits-dir", default=".")
args = parser.parse_args()
here = Path(__file__).resolve().parent
cases = json.loads((here / "cases.json").read_text())
result = subprocess.run(
    [args.cleave, "--traits-dir", args.traits_dir, "--format", "json"]
    + [str(here / case["path"]) for case in cases["fixtures"]],
    text=True, capture_output=True, check=True,
)
decoder = json.JSONDecoder()
remaining = result.stdout.strip()
files = {}
while remaining:
    value, end = decoder.raw_decode(remaining)
    for file in value.get("files", []):
        files[Path(file["path"]).name] = file
    remaining = remaining[end:].lstrip()
for case in cases["fixtures"]:
    traits = files[case["path"]]["traits"]
    ids = {t["id"] for t in traits}
    assert not ids.intersection(cases["retired"]), (case["path"], ids)
    assert ids.intersection(cases["traits"]) == set(case["matched"]), (
        case["path"], ids.intersection(cases["traits"]), case["matched"]
    )
    if case["path"] != "obfuscated-task.js":
        assert not any(t["crit"] >= 4 for t in traits), (case["path"], traits)
print(f"Passed {len(cases['fixtures'])} trait readability controls")
