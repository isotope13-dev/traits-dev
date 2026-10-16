"""Regression checks for user registry overrides beside auto-elevation triggers."""
import json
import os
from pathlib import Path
import subprocess

fixtures = Path(__file__).resolve().parent
root = fixtures.parents[2]
result = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(root),
     "--format", "json", *map(str, sorted(fixtures.glob("*.ps1"))),
     *map(str, sorted(fixtures.glob("*.py")))],
    check=True, capture_output=True, text=True,
)
remaining = result.stdout.lstrip()
decoder = json.JSONDecoder()
reports = {}
while remaining:
    report, end = decoder.raw_decode(remaining)
    remaining = remaining[end:].lstrip()
    for item in report.get("files", []):
        reports[Path(item["path"]).name] = item.get("traits", [])

prefix = "objectives/privilege-escalation/elevation-control/uac-bypass/hijack::"
python_rules = {prefix + "python-silentcleanup-windir-hijack",
                prefix + "python-sdclt-folder-command-hijack"}
ps_rules = {prefix + "silentcleanup-windir-override",
            prefix + "powershell-sdclt-folder-uac-bypass"}
for name, expected in [("positive.py", python_rules), ("positive.ps1", ps_rules)]:
    hostile = {t["id"] for t in reports[name] if t["crit"] == 5}
    assert expected <= hostile, (name, expected - hostile)

for name in ["ordinary-task.ps1", "read-environment.py", "machine-hive.py",
             "different-task.py", "comments.py", "comments.ps1"]:
    ids = {t["id"] for t in reports[name]}
    assert not ids & (python_rules | ps_rules), (name, ids & (python_rules | ps_rules))
print("PASS: both positive samples meet hostile floors; six controls exclude hijacks")
