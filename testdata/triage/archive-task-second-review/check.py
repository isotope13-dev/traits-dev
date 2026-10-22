#!/usr/bin/env python3
"""Keep maintenance installers suspicious and filename references neutral."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
TASK = "objectives/persistence/system/scheduled-task::"
NAME = "micro-behaviors/fs/path/basename::radmin-interface-executable-reference"
OLD = "well-known/dual-use/remote-admin/radmin::radmin-interface-executable-reference"

# Scan outside testdata so test-directory exclusions cannot hide a regression.
# These sources are only scanned, never executed.
with tempfile.TemporaryDirectory(prefix=".archive-task-review-", dir=ROOT) as work:
    work = Path(work)
    installer = (ROOT / "testdata/triage/archive-task-review/maintenance-setup.py").read_text()
    (work / "maintenance.py").write_text(installer)
    argv = 'subprocess.run(["schtasks", "/create", "/tn", "MaintenanceUpdates", "/sc", "hourly", "/mo", "3", "/tr", action, "/f"], check=True)'
    command = ('command = f\'schtasks /create /tn "MaintenanceUpdates" /tr "{action}" /sc HOURLY /mo 3 /f\'\n'
               'subprocess.run(command, shell=True, check=True)')
    assert argv in installer
    (work / "maintenance-shell.py").write_text(installer.replace(argv, command))
    for name, value in (("reference.py", "FamItrfc.exe"),
                        ("variant.py", "FAMITRF2.EXE"),
                        ("miss.py", "FamItrfx.exe")):
        (work / name).write_text("executable = " + repr(value) + "\n")
    result = subprocess.run(
        [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
         "--format", "json", str(work)],
        check=True, capture_output=True, text=True,
    )
    assert not result.stderr.strip(), result.stderr
    decoder = json.JSONDecoder()
    remaining = result.stdout.strip()
    findings = {}
    while remaining:
        report, end = decoder.raw_decode(remaining)
        remaining = remaining[end:].lstrip()
        for f in report["files"]:
            findings[Path(f["path"]).name] = {t["id"]: t["crit"] for t in f["traits"]}
    for name in ("maintenance.py", "maintenance-shell.py"):
        traits = findings[name]
        assert traits[TASK + "python-self-deleting-appdata-forced-repeat-task"] == 4
        assert traits["objectives/evasion/self-delete/file/script::self-delete-python"] == 4
        assert 5 not in traits.values(), (name, traits)
    for name in ("reference.py", "variant.py"):
        assert findings[name][NAME] == 3
        assert OLD not in findings[name]
        assert not any(t.startswith("well-known/dual-use/remote-admin/") for t in findings[name])
    assert NAME not in findings["miss.py"] and OLD not in findings["miss.py"]

print("Five maintenance-installer and executable-filename controls passed")
