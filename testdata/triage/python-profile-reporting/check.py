"""Scan fixture copies outside testing paths; never execute their contents."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
cases = json.loads((HERE / "cases.json").read_text())["fixtures"]
with tempfile.TemporaryDirectory(prefix=".profile-reporting-", dir=ROOT) as directory:
    paths = []
    for case in cases:
        path = Path(directory) / Path(case["path"]).name
        path.write_bytes((ROOT / case["path"]).read_bytes())
        paths.append(str(path))
    result = subprocess.run(
        [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
         "analyze", "--format", "json", *paths],
        check=True, capture_output=True, text=True,
    )
    # Multiple targets currently produce adjacent JSON report objects.
    remaining = result.stdout
    decoder = json.JSONDecoder()
    files = {}
    while remaining.strip():
        report, end = decoder.raw_decode(remaining.lstrip())
        remaining = remaining.lstrip()[end:]
        for file in report["files"]:
            files[Path(file["path"]).name] = file
    for case in cases:
        file = files[Path(case["path"]).name]
        ids = {trait["id"] for trait in file["traits"]}
        missing = set(case["matched"]) - ids
        unexpected = set(case["not_matched"]) & ids
        elevated = [trait["id"] for trait in file["traits"] if trait["crit"] > 3]
        assert not (missing or unexpected or elevated), (
            case["case_id"], missing, unexpected, elevated
        )
        print("PASS", case["case_id"])
