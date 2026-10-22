"""Check source-to-send bindings and nearby nonmatching variants."""
import json
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[3]
cases = json.loads(Path(__file__).with_name("cases.json").read_text())["fixtures"]
result = subprocess.run(
    [sys.argv[1] if len(sys.argv) > 1 else "cleave", "--traits-dir", ".",
     "--json", *[case["path"] for case in cases]],
    cwd=root, capture_output=True, text=True,
)
if result.returncode:
    raise RuntimeError(result.stderr)
reports = [json.loads(line) for line in result.stdout.splitlines() if line.strip()]
observed = {
    file["path"]: {trait["id"] for trait in file.get("traits", [])}
    for report in reports for file in report["files"]
}
failures = []
for case in cases:
    assert case["path"] in observed, case["path"]
    found = observed[case["path"]]
    for trait in case["matched"]:
        if trait not in found:
            failures.append((case["path"], "missing", trait))
    for trait in case["not_matched"]:
        if trait in found:
            failures.append((case["path"], "unexpected", trait))
assert not failures, failures
print(f"Passed {len(cases)} focused cases")
