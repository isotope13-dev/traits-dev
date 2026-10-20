"""Scan fixtures without executing their code; check emitted trait contracts."""
import json
import subprocess
from pathlib import Path

folder = Path(__file__).parent
cases = json.loads((folder / "cases.json").read_text())["fixtures"]
result = subprocess.run(
    ["cleave", "--format", "json", *[case["path"] for case in cases]],
    capture_output=True,
    text=True,
    check=True,
)
reports = []
pending = result.stdout.strip()
decoder = json.JSONDecoder()
while pending:
    document, end = decoder.raw_decode(pending)
    reports.extend(document["files"])
    pending = pending[end:].lstrip()
for case in cases:
    matching = [report for report in reports if report["path"].endswith(case["path"])]
    assert len(matching) == 1, case["path"]
    traits = matching[0].get("traits", [])
    ids = {trait["id"] for trait in traits}
    missing = set(case.get("matched", [])) - ids
    unexpected = set(case.get("not_matched", [])) & ids
    assert not missing, (case["path"], "missing", missing)
    assert not unexpected, (case["path"], "unexpected", unexpected)
    assert max((trait["crit"] for trait in traits), default=0) <= case.get("max_crit", 5), case["path"]
    print("PASS", case["path"])
