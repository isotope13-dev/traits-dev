import json
import subprocess
from pathlib import Path

cases = json.loads(Path(__file__).with_name("cases.json").read_text())["fixtures"]
result = subprocess.run(["cleave", "--traits-dir", ".", "--format", "json", *[c["path"] for c in cases]], capture_output=True, text=True)
assert result.returncode == 0, result.stderr
reports = []
remaining = result.stdout.lstrip()
while remaining:
    item, end = json.JSONDecoder().raw_decode(remaining)
    reports.extend(item["files"])
    remaining = remaining[end:].lstrip()
for case in cases:
    report = next(r for r in reports if r["path"].endswith(case["path"]))
    traits = {t["id"]: t for t in report.get("traits", [])}
    for trait in case.get("matched", []):
        assert trait in traits, (case["path"], "missing", trait)
    for trait in case.get("not_matched", []):
        assert trait not in traits, (case["path"], "unexpected", trait)
    for trait, level in case.get("levels", {}).items():
        assert traits[trait]["crit"] == level, (case["path"], trait, traits[trait]["crit"])
    if "max_suspicious" in case:
        assert sum(t["crit"] >= 4 for t in traits.values()) <= case["max_suspicious"], (case["path"], [(k,t["crit"]) for k,t in traits.items() if t["crit"] >= 4])
print(f"Passed {len(cases)} focused cases")
