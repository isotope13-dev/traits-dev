"""Check request/receiver binding and per-call whitespace filtering."""
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
cases = json.loads((HERE / "cases.json").read_text())["fixtures"]
result = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
     "--format", "json", *[case["path"] for case in cases]],
    cwd=ROOT, capture_output=True, text=True, check=True,
)
decoder = json.JSONDecoder()
remaining = result.stdout
reports = {}
while remaining.strip():
    item, end = decoder.raw_decode(remaining.lstrip())
    remaining = remaining.lstrip()[end:]
    for report in item.get("files", []):
        reports[report["path"]] = report

failures = []
for case in cases:
    report = reports[case["path"]]
    actual = {trait["id"] for trait in report.get("traits", [])}
    missing = set(case["matched"]) - actual
    unexpected = set(case["not_matched"]) & actual
    if missing or unexpected:
        failures.append((case["path"], missing, unexpected))
if failures:
    raise SystemExit(f"Trait regression failures: {failures}")
print(f"PASS: {len(cases)} focused controls")
