"""Run rule controls outside test-directory suppressors, without executing them."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
cases = json.loads((HERE / "cases.json").read_text())
scratch = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT
with tempfile.TemporaryDirectory(prefix="ci-source-controls-", dir=scratch) as tmp:
    stage = Path(tmp)
    for case in cases:
        dest = stage / case["file"]
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(HERE / case["file"], dest)
    result = subprocess.run(
        [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
         "--format", "jsonl", str(stage)],
        check=False, capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr
    assert not result.stderr.strip(), result.stderr
    decoder = json.JSONDecoder()
    remaining = result.stdout
    files = {}
    while remaining.strip():
        remaining = remaining.lstrip()
        report, end = decoder.raw_decode(remaining)
        remaining = remaining[end:]
        for file in report["files"]:
            files[file["path"]] = {t["id"]: t["crit"] for t in file.get("traits", [])}
    for case in cases:
        actual = files[str(stage / case["file"])]
        missing = set(case.get("present", [])) - actual.keys()
        unwanted = set(case.get("absent", [])) & actual.keys()
        assert not missing and not unwanted, (case["file"], missing, unwanted)
        for trait, criticality in case.get("criticality", {}).items():
            assert actual[trait] == criticality, (case["file"], trait, actual[trait])
        for trait in case.get("debug_present", []):
            # Unconsumed baseline observations can be stripped from reports.
            trace = subprocess.run(
                [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
                 "test-rules", str(stage / case["file"]), "--rules", trait],
                check=True, capture_output=True, text=True,
            )
            assert "\nMATCHED " + trait in trace.stdout, trace.stdout + trace.stderr
        print("PASS", case["file"])
