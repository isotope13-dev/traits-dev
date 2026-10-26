"""Scan source controls; never execute their AppleScript or shell commands."""
import json
import os
from pathlib import Path
import subprocess


RULE = (
    "objectives/exfiltration/stealer/system-info/profile::"
    "password-phishing-upload-with-system-profiling"
)
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent

for name, expected in {
    "phish-upload-profile.applescript": True,
    "ordinary-upload-profile.applescript": False,
    "phish-upload-only.applescript": False,
    "profile-only.applescript": False,
}.items():
    result = subprocess.run(
        [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
         "--format", "json", str(HERE / name)],
        capture_output=True, text=True, check=True,
    )
    report = json.loads(result.stdout)
    traits = {
        trait["id"]
        for file in report["files"]
        for trait in file.get("traits", [])
    }
    assert (RULE in traits) == expected, (name, expected)
    print(f"PASS {name}: matched={expected}")
