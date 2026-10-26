#!/usr/bin/env python3
"""Static Defender-profile controls. Never execute the supplied PE.

Usage: python3 check.py <reviewed-keylogger.exe> <scratch-directory>
"""
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
PREFIX = "objectives/evasion/anti-av/platform/defender::"
DISABLE = PREFIX + "managed-keylogger-defender-disable-command"
EXCLUDE = PREFIX + "managed-backdoor-or-keylogger-defender-exclusions"


def scan(path):
    result = subprocess.run(
        [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
         "--format", "json", str(path)],
        check=True, capture_output=True, text=True)
    report = json.loads(result.stdout)
    return {t["id"] for f in report["files"] for t in f.get("traits", [])}


def main():
    sample, scratch = map(Path, sys.argv[1:])
    scratch.mkdir(parents=True, exist_ok=True)
    original = sample.read_bytes()
    variants = [
        ("original", [], {DISABLE, EXCLUDE}),
        ("no-recorder", [("WH_KEYBOARD_LL", "XX_KEYBOARD_LL", "ascii")], set()),
        ("no-hidden-setup", [("set_CreateNoWindow", "set_CreateXXWindow", "ascii")], set()),
        ("no-disable", [("Set-MpPreference", "Get-MpPreference", "utf-16le")], {EXCLUDE}),
        ("no-exclusion", [("Add-MpPreference", "Get-MpPreference", "utf-16le")], {DISABLE}),
    ]
    checks = []
    for name, replacements, expected in variants:
        data = original
        for old, new, encoding in replacements:
            old, new = old.encode(encoding), new.encode(encoding)
            assert len(old) == len(new) and old in data, name
            data = data.replace(old, new)
        path = scratch / (name + ".exe")
        path.write_bytes(data)
        matched = scan(path) & {DISABLE, EXCLUDE}
        assert matched == expected, (name, matched, expected)
        checks.append({"case": name, "matched": sorted(matched)})
        print("PASS", name, flush=True)
    # Real benign CLR assemblies, including a no-op native-interop control.
    for name in ["managed-native-interop-only.exe", "managed-status-stubs-only.exe",
                 "dotnet-default-manifest.dll"]:
        matched = scan(ROOT / "testdata" / "benign" / name)
        assert not matched & {DISABLE, EXCLUDE}, name
        checks.append({"case": name, "matched": []})
        print("PASS", name, flush=True)
    (scratch / "checks.json").write_text(json.dumps(checks, indent=2) + "\n")


if __name__ == "__main__":
    main()
