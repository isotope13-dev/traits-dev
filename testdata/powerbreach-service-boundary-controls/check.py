"""Check static trigger distinctions and service-reference exclusion scope."""
import json
import os
from pathlib import Path
import subprocess

fixtures = Path(__file__).resolve().parent
traits = fixtures.parent.parent
cases = json.loads((fixtures / "cases.json").read_text())
result = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(traits), "--json"]
    + [str(fixtures / case["file"]) for case in cases],
    capture_output=True, text=True, check=True,
)
reports = {}
for line in result.stdout.splitlines():
    report = json.loads(line)
    reports[Path(report["files"][0]["path"]).name] = {
        trait["id"] for file in report["files"]
        for trait in file.get("traits", [])
    }
for case in cases:
    ids = reports[case["file"]]
    missing = set(case.get("present", [])) - ids
    unexpected = set(case.get("absent", [])) & ids
    assert not missing, (case["file"], "missing", sorted(missing))
    assert not unexpected, (case["file"], "unexpected", sorted(unexpected))
    print("PASS", case["file"])
