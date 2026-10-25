"""Run focused protocol, source-syntax, and MPEG-TS regression controls."""
import json
import os
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parent
repo = root.parents[2]
cases = json.loads((root / "cases.json").read_text())["fixtures"]
proc = subprocess.run([os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(repo),
                       "--format", "json", *[str(root / c["path"]) for c in cases]],
                      check=True, capture_output=True, text=True)
# Cleave streams adjacent JSON report objects for multiple input paths.
decoder = json.JSONDecoder()
remaining = proc.stdout
files = {}
while remaining.strip():
    report, end = decoder.raw_decode(remaining.lstrip())
    remaining = remaining.lstrip()[end:]
    files.update({Path(f["path"]).name: f for f in report["files"]})
for case in cases:
    traits = files[case["path"]].get("traits", [])
    ids = {t["id"] for t in traits}
    assert set(case.get("matched", [])) <= ids, (case["path"], "missing", ids)
    assert not set(case.get("not_matched", [])) & ids, (case["path"], "unexpected", ids)
    if case.get("no_elevated"):
        assert all(t["crit"] < 4 for t in traits), case["path"]
print(f"{len(cases)} focused controls passed")
