"""Exercise trait boundaries without executing fixture code."""
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
cases = json.loads((HERE / "cases.json").read_text())
result = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
     "--format", "json", *[str((HERE / c["path"]).resolve()) for c in cases]],
    text=True, capture_output=True, check=True,
)
reports = []
remaining = result.stdout
decoder = json.JSONDecoder()
while remaining.strip():
    report, end = decoder.raw_decode(remaining.lstrip())
    remaining = remaining.lstrip()[end:]
    reports.append(report)
assert len(reports) == len(cases), (len(reports), len(cases), result.stderr)
for case, report in zip(cases, reports):
    findings = {t["id"]: t for f in report["files"] for t in f.get("traits", [])}
    missing = set(case["required"]) - findings.keys()
    unexpected = set(case["forbidden"]) & findings.keys()
    assert not missing and not unexpected, (case["path"], missing, unexpected)
    if "max_hostile" in case:
        hostile = sum(t["crit"] == 5 for t in findings.values())
        assert hostile <= case["max_hostile"], (case["path"], hostile)
print(f"{len(cases)} focused cases passed")
