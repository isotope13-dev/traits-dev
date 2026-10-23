"""Scan inert source; preserve attack detections and reject build-task FPs."""
import json
import os
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
cases = json.loads((HERE / "cases.json").read_text())["cases"]
result = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT), "--json",
     *[str(HERE / case["path"]) for case in cases]],
    check=True, text=True, capture_output=True,
)
reports = {}
for line in result.stdout.splitlines():
    for file in json.loads(line).get("files", []):
        reports[Path(file["path"]).name] = file
for case in cases:
    traits = {trait["id"]: trait["crit"]
              for trait in reports[case["path"]].get("traits", [])}
    for trait, criticality in case.get("required", {}).items():
        assert traits.get(trait) == criticality, (case["path"], trait, traits)
    assert not set(case.get("absent", [])).intersection(traits), case["path"]
    assert max(traits.values(), default=0) <= case["max"], (case["path"], traits)
print(f"PASS: {len(cases)} MSBuild, policy, and concealed-evaluation controls")
