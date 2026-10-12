import json, subprocess
from pathlib import Path
cases = json.loads(Path(__file__).with_name("cases.json").read_text())
result = subprocess.run(["cleave", "--traits-dir", ".", "--json", *[c["path"] for c in cases]], check=True, capture_output=True, text=True)
files = {f["path"]: f for line in result.stdout.splitlines() for f in json.loads(line)["files"]}
for case in cases:
    file = files.get(case["path"]) or files[str(Path(case["path"]).resolve())]
    traits = {t["id"]: t for t in file["traits"]}
    assert all(t in traits for t in case["required"]), (case["path"], "missing", case["required"])
    hostile = [t for t in traits.values() if t["crit"] == 5]
    assert len(hostile) == case["hostile_count"], (case["path"], hostile)
    if case["forbid_installer"]:
        assert "micro-behaviors/process/create/installer::rotating-downloadandinstall-call" not in traits, case["path"]
print(f"Passed {len(cases)} positive and near-miss fixtures")
