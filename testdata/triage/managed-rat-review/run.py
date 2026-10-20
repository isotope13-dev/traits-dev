"""Check VM-display positives and independent manufacturer/GPU near misses."""
import json
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[3]
cases = json.loads(Path(__file__).with_name("cases.json").read_text())["fixtures"]
result = subprocess.run(
    [sys.argv[1] if len(sys.argv) > 1 else "cleave", "--traits-dir", str(root),
     "--format", "json", *[str(root / case["path"]) for case in cases]],
    check=True, text=True, capture_output=True,
)
files = []
remaining = result.stdout.strip()
decoder = json.JSONDecoder()
while remaining:
    report, end = decoder.raw_decode(remaining)
    files.extend(report["files"])
    remaining = remaining[end:].lstrip()
reports = {Path(f["path"]).name: {t["id"] for t in f["traits"]} for f in files}
for case in cases:
    actual = reports[Path(case["path"]).name]
    missing = set(case["required_emitted"]) - actual
    unexpected = set(case["forbidden_emitted"]) & actual
    if missing or unexpected:
        raise AssertionError((case["case_id"], missing, unexpected))
print(f"PASS: {len(cases)} VM-display controls")
