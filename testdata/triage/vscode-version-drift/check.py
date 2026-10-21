"""Focused controls for nested installs, identity facts, and input markup."""
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
CASES = json.loads(Path(__file__).with_name("cases.json").read_text())["cases"]
result = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
     "--format", "jsonl", *[str(ROOT / case["path"]) for case in CASES]],
    capture_output=True, text=True, check=True,
    env=dict(os.environ, CLEAVE_VALIDATE="0"),
)
observed = {}
for line in result.stdout.splitlines():
    for entry in json.loads(line)["files"]:
        observed[str(Path(entry["path"]).resolve())] = {
            trait["id"] for trait in entry.get("traits", [])
        }
for case in CASES:
    actual = observed[str((ROOT / case["path"]).resolve())]
    missing = set(case["matched"]) - actual
    unexpected = set(case["not_matched"]) & actual
    assert not missing and not unexpected, (case["path"], missing, unexpected)
print(f"PASS {len(CASES)} focused cases")
