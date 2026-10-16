"""Static controls for request evaluation, crypto and HTTP error masking."""
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
cases = json.loads((HERE / "cases.json").read_text())
result = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT), "--json",
     *[str(HERE / name) for name in cases]],
    env=dict(os.environ, CLEAVE_SKIP_CACHE="1"),
    capture_output=True, text=True, check=True,
)
assert "warning" not in result.stderr.lower(), result.stderr
checked = set()
for line in result.stdout.splitlines():
    for report in json.loads(line).get("files", []):
        name = Path(report["path"]).name
        case = cases[name]
        traits = {item["id"]: item["crit"] for item in report["traits"]}
        assert set(case.get("required", [])) <= traits.keys(), (name, traits)
        assert not set(case.get("forbidden", [])) & traits.keys(), (name, traits)
        assert sum(crit == 5 for crit in traits.values()) >= case.get("hostile_floor", 0), (name, traits)
        checked.add(name)
assert checked == cases.keys(), checked
print(f"Passed {len(checked)} encrypted-request webshell controls")
