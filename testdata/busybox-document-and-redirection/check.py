"""Check original attack coverage and documentation/redirection boundaries."""
import json
import os
from pathlib import Path
import subprocess

here = Path(__file__).resolve().parent
root = here.parents[1]
cases = json.loads((here / "cases.json").read_text())
result = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(root), "--json",
     *[str(here / case["file"]) for case in cases]],
    cwd=root, text=True, capture_output=True, check=True,
)
remaining = result.stdout.lstrip()
decoder = json.JSONDecoder()
observed = {}
while remaining:
    report, end = decoder.raw_decode(remaining)
    remaining = remaining[end:].lstrip()
    for file in report["files"]:
        observed[Path(file["path"]).name] = file.get("traits", [])

for case in cases:
    traits = observed[case["file"]]
    actual = {trait["id"] for trait in traits}
    missing = set(case["required"]) - actual
    unexpected = set(case["forbidden"]) & actual
    if case.get("forbid_hostile"):
        unexpected |= {trait["id"] for trait in traits if trait["crit"] >= 5}
    assert not missing and not unexpected, (case["file"], missing, unexpected)
print(f"Passed {len(cases)} original and boundary controls")
