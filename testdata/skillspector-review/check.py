"""Check executable scanner fixtures separately from the strict benign corpus."""
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = sys.argv[1] if len(sys.argv) > 1 else "cleave"
cases = json.loads(Path(__file__).with_name("cases.json").read_text())
for case in cases:
    result = subprocess.run(
        [CLEAVE, "--traits-dir", str(ROOT), "--format", "json", str(ROOT / case["path"])],
        cwd=ROOT, capture_output=True, text=True, check=True,
    )
    assert not result.stderr.strip(), result.stderr
    report = json.loads(result.stdout)
    traits = report["files"][0].get("traits", [])
    ids = {trait["id"] for trait in traits}
    for level, name in [(5, "hostile"), (4, "suspicious")]:
        actual = sum(trait["crit"] == level for trait in traits)
        assert actual == case[name], (case["path"], name, actual, case[name])
    assert set(case.get("required", [])) <= ids, case["path"]
    assert not set(case.get("forbidden", [])) & ids, case["path"]
    print("PASS " + case["path"])
