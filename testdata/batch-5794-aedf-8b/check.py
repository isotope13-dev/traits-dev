"""Scan static fixtures; never execute their contents."""
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
PATH_TRAIT = "micro-behaviors/fs/path/config/autorun::app-bundled-launchd-path-reference"
HID_TRAIT = "micro-behaviors/hardware/input/device::winrt-hid-output-report"
EXPECTED = {
    "bundled-launchd.sh": {PATH_TRAIT},
    "bundled-launchdaemon.sh": {PATH_TRAIT},
    "unrelated-directory.sh": set(),
    "winrt-hid.ts": {HID_TRAIT},
    "winrt-hid-mentions.ts": set(),
}
ATTACKS = {
    "testdata/hostile/validated-installer-clipboard.sh": {
        "objectives/credential-access/phishing/ui::shell-validated-dialog-input-file": 5,
        "objectives/exfiltration/stealer/input::shell-validated-password-clipboard-exfil": 5,
        "objectives/persistence/system/launchd/source::shell-phishing-launchagent-install": 5,
        "objectives/credential-access/phishing/lure::applescript-password-phish-validate": 4,
        "objectives/credential-access/phishing/ui::shell-validated-dialog-store-flow": 4,
    },
    "testdata/hostile/supply-chain-corpus/brew/brew-basaltstack-post-install-plist-macos.rb": {
        "objectives/supply-chain/trojanized/app/remote-install::formula-launchagent-shell-loader": 5,
        "micro-behaviors/os/service/launchagent::source-launchagent-remote-shell-autorun": 4,
    },
}
paths = [str(HERE / name) for name in EXPECTED] + list(ATTACKS)
result = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
     "--format", "json", *paths],
    cwd=ROOT, text=True, capture_output=True, check=True,
)
decoder = json.JSONDecoder()
remaining = result.stdout.strip()
files = {}
while remaining:
    report, end = decoder.raw_decode(remaining)
    files.update((f["path"], f) for f in report["files"])
    remaining = remaining[end:].strip()
for name, expected in EXPECTED.items():
    traits = files[str(HERE / name)].get("traits", [])
    actual = {t["id"] for t in traits if t["id"] in {PATH_TRAIT, HID_TRAIT}}
    assert actual == expected, (name, actual, expected)
    assert all(t["crit"] == 3 for t in traits if t["id"] in expected)
    assert not any(t["crit"] >= 4 for t in traits), name
for path, expected in ATTACKS.items():
    actual = {t["id"]: t["crit"] for t in files[path].get("traits", [])
              if t["crit"] >= 4}
    assert actual == expected, (path, actual, expected)
print("Passed 5 focused fixtures and 2 existing attack fixtures.")
