"""Static detection regressions; none of the fixture programs are executed."""
import argparse
import json
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("--report", type=Path)
args = parser.parse_args()
fixtures = Path(__file__).resolve().parent
root = fixtures.parents[2]
if args.report:
    data = args.report.read_text()
else:
    data = subprocess.check_output(
        ["cleave", "--traits-dir", str(root), "--format", "json", str(fixtures)],
        text=True,
    )
decoder = json.JSONDecoder()
reports = {}
while data.strip():
    report, end = decoder.raw_decode(data.lstrip())
    data = data.lstrip()[end:]
    for file in report["files"]:
        reports[Path(file["path"]).name] = {
            trait["id"] for trait in file.get("traits", [])
        }
cases = json.loads((fixtures / "cases.json").read_text())["fixtures"]
for case in cases:
    traits = reports[case["path"]]
    missing = set(case["required"]) - traits
    unexpected = set(case["forbidden"]) & traits
    assert not missing and not unexpected, (case["path"], missing, unexpected)
print(f"Passed {len(cases)} static detection controls")
