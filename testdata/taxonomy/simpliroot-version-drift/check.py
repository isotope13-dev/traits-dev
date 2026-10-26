"""Static regression controls for the SimpliRoot version-drift review."""
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
cases = json.loads((HERE / "cases.json").read_text())
result = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT), "--json",
     *[str(HERE / name) for name in cases]],
    capture_output=True, text=True, check=True,
)
assert "warning" not in result.stderr.lower(), result.stderr
checked = set()
remaining = result.stdout
decoder = json.JSONDecoder()
while remaining.strip():
    parsed, end = decoder.raw_decode(remaining.lstrip())
    remaining = remaining.lstrip()[end:]
    for report in parsed.get("files", []):
        name = Path(report["path"]).name
        case = cases[name]
        traits = {item["id"]: item["crit"] for item in report.get("traits", [])}
        for trait, criticality in case.get("required", {}).items():
            assert traits.get(trait) == criticality, (name, trait, traits)
        assert not set(case.get("forbidden", [])) & traits.keys(), (name, traits)
        for key, criticality in [("suspicious", 4), ("hostile", 5)]:
            if key in case:
                assert sum(c == criticality for c in traits.values()) == case[key], (name, traits)
        checked.add(name)
assert checked == cases.keys(), checked
print(f"Passed {len(checked)} SimpliRoot version-drift controls")
