"""Disclosed QVI panels must not be convicted as Amazon credential harvesters.

The undisclosed twin keeps the hostile verdict; the disclosed twin (both QVI
backends plus the shareInsights consent key in one file) loses the hostile
and cookie/auth suspicious traits. The deliberately unexcepted account
e-mail upload is not asserted here: its remote-host leg is suppressed for
test-directory paths, so it is verified on the real panel build instead.
"""
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
cases = json.loads((HERE / "cases.json").read_text())
reports = []
for name in cases:
    result = subprocess.run(
        [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
         "--json", str(HERE / name)],
        env=dict(os.environ),
        capture_output=True, text=True, check=True,
    )
    for line in result.stdout.splitlines():
        reports.extend(json.loads(line).get("files", []))
checked = set()
for report in reports:
        name = Path(report["path"]).name
        case = cases[name]
        traits = {item["id"]: item["crit"] for item in report["traits"]}
        assert set(case.get("required", [])) <= traits.keys(), (name, sorted(traits))
        assert not set(case.get("forbidden", [])) & traits.keys(), (name, sorted(traits))
        hostile = sum(crit == 5 for crit in traits.values())
        suspicious = sum(crit == 4 for crit in traits.values())
        assert hostile >= case.get("hostile_min", 0), (name, hostile, sorted(traits))
        assert hostile <= case.get("hostile_max", 99), (name, hostile, sorted(traits))
        assert suspicious <= case.get("suspicious_max", 99), (name, suspicious, sorted(traits))
        checked.add(name)
assert checked == cases.keys(), checked
print(f"Passed {len(checked)} QVI Amazon disclosed-panel controls")
