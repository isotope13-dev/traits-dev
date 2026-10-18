import json
import os
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[3]
base = Path(__file__).resolve().parent
cases = json.loads((base / "cases.json").read_text())["fixtures"]
result = subprocess.run([os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(root),
                         "--format=json", *[str(root / c["path"]) for c in cases]],
                        text=True, capture_output=True, check=True)
reports = []
decoder = json.JSONDecoder()
payload = result.stdout.lstrip()
while payload:
    report, consumed = decoder.raw_decode(payload)
    reports.append(report)
    payload = payload[consumed:].lstrip()
files = {Path(f["path"]).name: f for report in reports for f in report["files"]}
failures = []
for case in cases:
    found = {t["id"] for t in files[Path(case["path"]).name].get("traits", [])}
    missing = set(case.get("required_emitted", [])) - found
    unexpected = set(case.get("forbidden_emitted", [])) & found
    if missing or unexpected:
        failures.append({"case": case["case_id"], "missing": sorted(missing),
                         "unexpected": sorted(unexpected)})
print(json.dumps({"cases": len(cases), "failures": failures}, indent=2))
if result.stderr:
    print(result.stderr, file=sys.stderr)
sys.exit(bool(failures))
