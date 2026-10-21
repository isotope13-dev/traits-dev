#!/usr/bin/env python3
"""Check task-installer severity and parsed ctypes calls without execution."""
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
TASK = "objectives/persistence/system/scheduled-task::"
MUTEX = "micro-behaviors/process/sync/mutex::"
OLD = "objectives/command-and-control/dropper/delivery/execute-download/script::python-self-deleting-archive-task-dropper"

# Copy outside testdata: testing-directory suppressors must not mask the
# severity regression in the Python installer. The files are only scanned.
with tempfile.TemporaryDirectory(prefix=".archive-task-review-", dir=ROOT) as work:
    work = Path(work)
    for name in ("maintenance-setup.py", "maintenance-setup.ps1",
                 "mutex-call.py", "mutex-reference.py"):
        shutil.copyfile(HERE / name, work / name)
    result = subprocess.run(
        [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
         "--format", "json", str(work)],
        check=True, text=True, capture_output=True,
    )
    assert not result.stderr.strip(), result.stderr
    decoder = json.JSONDecoder()
    remaining = result.stdout.strip()
    findings = {}
    while remaining:
        report, end = decoder.raw_decode(remaining)
        remaining = remaining[end:].lstrip()
        for f in report["files"]:
            findings[Path(f["path"]).name] = {
                t["id"]: t["crit"] for t in f["traits"]
            }

    for name, specific in (
        ("maintenance-setup.py", "python-appdata-self-deleting-archive-task-loader"),
        ("maintenance-setup.ps1", "powershell-self-deleting-archive-variable-task-loader"),
    ):
        traits = findings[name]
        assert 5 not in traits.values(), (name, "ordinary installer marked hostile")
        assert traits[TASK + specific] == 4
        broad = "python" if name.endswith(".py") else "powershell"
        assert traits[TASK + broad + "-self-deleting-archive-task-loader"] == 4
        assert OLD not in traits

    assert findings["mutex-call.py"][MUTEX + "python-ctypes-create-mutex"] == 3
    assert not any(t.startswith(MUTEX) for t in findings["mutex-reference.py"])
    assert 5 not in findings["mutex-call.py"].values()

print("4 archive-task and mutex boundary controls passed")
