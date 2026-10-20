"""Run the comment-padded loader positive and near-miss cases."""
import argparse
import json
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("--cleave", default="cleave")
parser.add_argument("--report")
args = parser.parse_args()
cases = json.loads(Path(__file__).with_name("cases.json").read_text())["cases"]
if args.report:
    data = Path(args.report).read_text()
else:
    data = subprocess.check_output(
        [args.cleave, "--traits-dir", ".", "--format", "json"]
        + [case["path"] for case in cases], text=True
    )
decoder = json.JSONDecoder()
files = {}
while data.strip():
    report, end = decoder.raw_decode(data.lstrip())
    data = data.lstrip()[end:]
    for file in report["files"]:
        files[str(Path(file["path"]).resolve())] = {
            trait["id"] for trait in file.get("traits", [])
        }
for case in cases:
    actual = files[str(Path(case["path"]).resolve())]
    missing = set(case["matched"]) - actual
    unexpected = set(case["not_matched"]) & actual
    assert not missing and not unexpected, (case["case_id"], missing, unexpected)
    print("PASS", case["case_id"])
