"""Verify reference placement, exclusions, and unchanged consuming rules."""
import json
import os
from pathlib import Path
import subprocess

cases = json.loads(Path(__file__).with_name("cases.json").read_text())["fixtures"]
engine = os.environ.get("CLEAVE", "cleave")
result = subprocess.run(
    [engine, "--traits-dir", ".", "--json", *[c["path"] for c in cases]],
    capture_output=True, text=True, check=True,
)
reports = [json.loads(line) for line in result.stdout.splitlines()]
assert len(reports) == len(cases), result.stderr
for case, report in zip(cases, reports):
    assert report["files"][0]["path"] == case["path"]
    ids = {t["id"] for f in report["files"] for t in f.get("traits", [])}
    missing = set(case["matched"]) - ids
    unexpected = set(case["not_matched"]) & ids
    assert not missing and not unexpected, (case["path"], missing, unexpected)
print(f"PASS: {len(cases)} reference-placement cases")
