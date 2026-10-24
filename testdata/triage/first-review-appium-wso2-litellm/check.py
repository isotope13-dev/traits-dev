"""Check focused controls without importing or executing any sample code.
Usage: python3 check.py --report /path/to/cleave-controls.jsonl
Generate report: cleave --traits-dir . --json testdata/triage/first-review-appium-wso2-litellm
"""
import argparse
import json
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--report", required=True, type=Path)
args = parser.parse_args()
base = Path(__file__).resolve().parent
files = {}
for line in args.report.read_text().splitlines():
    for file in json.loads(line).get("files", []):
        files[Path(file["path"]).resolve()] = file
cases = json.loads((base / "cases.json").read_text())
for case in cases:
    traits = files[base / case["path"]].get("traits", [])
    ids = {trait["id"] for trait in traits}
    assert set(case.get("required", [])) <= ids, (case["path"], "missing")
    assert not set(case.get("forbidden", [])) & ids, (case["path"], "unexpected")
    for severity, value in (("hostile", 5), ("suspicious", 4)):
        count = sum(trait["crit"] == value for trait in traits)
        assert count <= case.get("max_" + severity, count), (case["path"], severity, count)
print(f"{len(cases)} focused controls passed")
