"""Exercise shared command/instruction moves and retained lure coverage."""
import json
import os
from pathlib import Path
import subprocess

here = Path(__file__).resolve().parent
root = here.parents[2]
cases = json.loads((here / "cases.json").read_text())
result = subprocess.run(
    ["atomscan", "--no-update", "--analyze", "local", "--mode", "slow",
     "--follow=none", "--format", "json", *[c["path"] for c in cases]],
    cwd=root,
    env={**os.environ, "SCAN_FETCH": "none", "CLEAVE_TRAITS_DIR": str(root)},
    text=True, capture_output=True, timeout=180,
)
# The scanner returns 1 when these positive attack controls are detected.
if result.returncode not in (0, 1):
    raise RuntimeError(result.stderr)
# splitlines() also splits valid Unicode characters inside JSON strings.
reports = [json.loads(line) for line in result.stdout.split("\n") if line.strip()]
files = {
    str(Path(f["path"]).resolve() if Path(f["path"]).is_absolute()
        else (root / f["path"]).resolve()): f
    for report in reports for f in report["raw"]["files"]
}
for case in cases:
    file = files[str((root / case["path"]).resolve())]
    traits = {t["id"]: t for t in file.get("traits", [])}
    assert set(case.get("required", [])) <= traits.keys(), case["path"]
    assert not set(case.get("forbidden", [])) & traits.keys(), case["path"]
    if "maximum_criticality" in case:
        assert all(t["crit"] <= case["maximum_criticality"]
                   for t in traits.values()), case["path"]
print(f"{len(cases)} controls passed")
