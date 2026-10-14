#!/usr/bin/env python3
"""Paramiko spray-and-exec controls.

Run `python3 testdata/ssh-spray-remote-exec/check.py
<scratch-directory>`. Fixtures are copied outside testdata so file-path
testing suppressors cannot mask the findings under test.
"""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

scratch = Path(sys.argv[1]) / "case"
scratch.mkdir(parents=True, exist_ok=True)
root = Path(__file__).resolve().parents[2]
for case in json.loads((Path(__file__).parent / "cases.json").read_text()):
    target = scratch / case["file"]
    shutil.copyfile(Path(__file__).parent / case["file"], target)
    result = subprocess.run(
        [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(root),
         "--format", "json", str(target)],
        env=dict(os.environ, CLEAVE_VALIDATE="0"), text=True,
        capture_output=True, check=True,
    )
    report = json.loads(result.stdout)
    ids = {trait["id"] for file in report["files"]
           for trait in file.get("traits", [])}
    assert set(case.get("present", [])) <= ids, case
    assert not set(case.get("absent", [])) & ids, case
    print("PASS", case["file"])
