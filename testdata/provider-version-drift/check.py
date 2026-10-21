"""Check inert package fixtures; never execute their JavaScript."""
import json
import os
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[2]
cases = json.loads(Path(__file__).with_name("cases.json").read_text())["fixtures"]
command = [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(root),
           "--format", "json", *[case["path"] for case in cases]]
result = subprocess.run(command, cwd=root, check=True, capture_output=True, text=True)
decoder = json.JSONDecoder()
remaining = result.stdout
reports = []
while remaining.strip():
    remaining = remaining.lstrip()
    report, end = decoder.raw_decode(remaining)
    reports.append(report)
    remaining = remaining[end:]
assert len(reports) == len(cases)
for case, report in zip(cases, reports):
    traits = {trait["id"] for file in report["files"]
              for trait in file.get("traits", [])}
    assert set(case["matched"]) <= traits, (case["path"], "missing", traits)
    assert not (set(case["not_matched"]) & traits), (case["path"], "unexpected")
    if "credential-transfer" not in case["path"]:
        assert all(trait["crit"] < 4 for file in report["files"]
                   for trait in file.get("traits", [])), case["path"]
    print("PASS", case["path"])
