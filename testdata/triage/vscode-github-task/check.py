"""Run source-binding and state-gate regressions without executing fixtures."""
import argparse
import json
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("--cleave", default="../cleave/target/release/cleave")
args = parser.parse_args()
here = Path(__file__).resolve().parent
root = here.parents[2]
cases = json.loads((here / "cases.json").read_text())
result = subprocess.run(
    [args.cleave, "--traits-dir", str(root), "--format", "json"]
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
    matched = {t["id"] for t in traits} & set(cases["traits"])
    assert matched == set(case["matched"]), (case["path"], matched, case["matched"])
    # These are execution-context observations, never standalone hostile proof.
    assert not any(t["crit"] >= 5 for t in traits), case["path"]
    if not any(t.startswith("objectives/") for t in case["matched"]):
        assert not any(t["crit"] >= 4 for t in traits), case["path"]
print(f"Passed {len(cases['fixtures'])} GitHub shell-task controls")
