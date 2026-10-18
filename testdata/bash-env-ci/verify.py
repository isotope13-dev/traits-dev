"""Check comment boundaries and preservation of the publish-secret consumers."""
import json
import os
from pathlib import Path
import subprocess


root = Path(__file__).resolve().parents[2]
cases = json.loads(Path(__file__).with_name("cases.json").read_text())["fixtures"]
result = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(root),
     "--format", "json", *[str(root / case["path"]) for case in cases]],
    capture_output=True, text=True,
)
assert result.returncode == 0, result.stderr
decoder = json.JSONDecoder()
remaining = result.stdout.strip()
findings = {}
while remaining:
    report, end = decoder.raw_decode(remaining)
    remaining = remaining[end:].lstrip()
    for file in report["files"]:
        findings[Path(file["path"]).resolve()] = {
            trait["id"] for trait in file.get("traits", [])
        }
for case in cases:
    actual = findings[(root / case["path"]).resolve()]
    missing = set(case["required_emitted"]) - actual
    unexpected = set(case["forbidden_emitted"]) & actual
    assert not missing and not unexpected, (case["path"], missing, unexpected)
    print("PASS", Path(case["path"]).name)
