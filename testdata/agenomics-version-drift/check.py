"""Scan controls outside testdata to avoid path-based test exclusions."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

root = Path(__file__).resolve().parents[2]
source = Path(__file__).resolve().parent
scratch = Path(sys.argv[1]).resolve()
scratch.mkdir(parents=True, exist_ok=True)
cases = json.loads((source / "cases.json").read_text())
for name in cases:
    shutil.copyfile(source / name, scratch / name)
result = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(root), "--json"]
    + [str(scratch / name) for name in cases],
    text=True, capture_output=True,

)
if result.returncode:
    raise RuntimeError(result.stderr)
reports = {}
for line in result.stdout.splitlines():
    for file in json.loads(line)["files"]:
        reports[Path(file["path"]).name] = file
for name, expected in cases.items():
    ids = {t["id"] for t in reports[name].get("traits", [])}
    missing = set(expected["matched"]) - ids
    extra = set(expected["not_matched"]) & ids
    assert not (missing or extra), (name, missing, extra)
    print("PASS", name)
print("Passed", len(cases), "static controls")
