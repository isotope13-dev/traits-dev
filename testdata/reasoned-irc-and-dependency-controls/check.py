"""Run static trait controls without executing fixture code."""
import json
from pathlib import Path
import subprocess

fixture_dir = Path(__file__).resolve().parent
traits_dir = fixture_dir.parent.parent
for case in json.loads((fixture_dir / "cases.json").read_text()):
    result = subprocess.run(
        ["cleave", "--traits-dir", str(traits_dir), "--format", "json",
         str(fixture_dir / case["file"])],
        capture_output=True, text=True, check=True,
    )
    report = json.loads(result.stdout)
    ids = {trait["id"] for file in report["files"]
           for trait in file.get("traits", [])}
    assert set(case.get("present", [])) <= ids, case
    assert not set(case.get("absent", [])) & ids, case
    print("PASS", case["file"])
