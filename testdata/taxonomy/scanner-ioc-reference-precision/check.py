"""Check reference-data exclusions and their execution near misses."""
import json
import os
from pathlib import Path
import subprocess


root = Path(__file__).resolve().parents[3]
here = Path(__file__).resolve().parent
cases = json.loads((here / "cases.json").read_text())
result = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(root),
     "--format", "jsonl", *[str(here / case["file"]) for case in cases]],
    check=True, capture_output=True, text=True,
)
assert not result.stderr.strip(), result.stderr
reports = {}
decoder = json.JSONDecoder()
remaining = result.stdout.strip()
while remaining:
    document, end = decoder.raw_decode(remaining)
    for report in document["files"]:
        reports[Path(report["path"]).name] = {
            trait["id"] for trait in report.get("traits", [])
        }
    remaining = remaining[end:].lstrip()

for case in cases:
    observed = reports[case["file"]]
    missing = set(case["required"]) - observed
    unwanted = set(case["forbidden"]) & observed
    assert not missing and not unwanted, (case["file"], missing, unwanted)
print(f"Passed {len(cases)} scanner reference and execution controls")
