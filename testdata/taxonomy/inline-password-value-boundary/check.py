"""Check password disclosures, instruction prose, and downstream lure rules."""
import json
import os
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[3]
cases = json.loads(Path(__file__).with_name("cases.json").read_text())["fixtures"]
result = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(root), "--json",
     *[str(root / case["path"]) for case in cases]],
    capture_output=True, text=True, check=True,
)
files = {}
for line in result.stdout.splitlines():
    for file in json.loads(line)["files"]:
        files[file["path"]] = {trait["id"] for trait in file.get("traits", [])}
for case in cases:
    found = files[str(root / case["path"])]
    missing = set(case["required_emitted"]) - found
    unexpected = set(case["forbidden_emitted"]) & found
    assert not missing and not unexpected, (case["path"], missing, unexpected)
print(f"{len(cases)} password disclosure boundary cases passed")
