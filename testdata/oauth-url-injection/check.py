"""Check OAuth injection coverage and near misses using emitted findings."""
import json
import os
from pathlib import Path
import subprocess


fixtures = Path(__file__).resolve().parent
root = fixtures.parents[1]
result = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(root),
     "--format", "jsonl", "analyze", str(fixtures)],
    capture_output=True, text=True,
)
if result.returncode:
    raise RuntimeError(result.stderr)
reports = {}
for line in result.stdout.splitlines():
    for report in json.loads(line).get("files", []):
        reports[Path(report["path"]).resolve()] = {
            trait["id"] for trait in report.get("traits", [])
        }
cases = json.loads((fixtures / "cases.json").read_text())["fixtures"]
for case in cases:
    actual = reports[(root / case["path"]).resolve()]
    missing = set(case["matched"]) - actual
    unexpected = set(case["not_matched"]) & actual
    assert not missing and not unexpected, (case["path"], missing, unexpected)
print(f"Passed {len(cases)} OAuth URL injection fixtures")
