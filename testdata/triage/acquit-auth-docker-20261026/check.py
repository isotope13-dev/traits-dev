"""Check semantic controls against saved cleave JSON or JSONL reports."""
import json
from pathlib import Path
import sys

cases = json.loads(Path(__file__).with_name("cases.json").read_text())
files = {}
for report_path in sys.argv[1:]:
    text = Path(report_path).read_text()
    try:
        reports = [json.loads(text)]
    except json.JSONDecodeError:
        reports = [json.loads(line) for line in text.splitlines() if line]
    for report in reports:
        for item in report["files"]:
            files[Path(item["path"]).name] = item
for name, expected in cases.items():
    item = files[name]
    traits = {trait["id"]: trait for trait in item["traits"]}
    for severity, level in (("hostile", 5), ("suspicious", 4)):
        if severity in expected:
            actual = sum(trait["crit"] == level for trait in traits.values())
            assert actual == expected[severity], (name, severity, actual)
    for trait in expected.get("required", []):
        assert trait in traits, (name, "missing", trait)
    for trait in expected.get("forbidden", []):
        assert trait not in traits, (name, "unexpected", trait)
print(f"Passed {len(cases)} behavioral controls")
