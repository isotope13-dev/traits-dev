#!/usr/bin/env python3
"""Check neutral task creation, cron relocation, and optional PE ablations."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
CLIP = "objectives/collection/clipboard/capture::managed-keylogger-clipboard-recording"
DEFENDER = "objectives/evasion/anti-av/platform/defender::managed-keylogger-defender-disable-command"
LOGON = "objectives/persistence/login/scheduled-task/cli::managed-keylogger-logon-task"


def scan(paths):
    result = subprocess.run(
        [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
         "--format", "jsonl", "analyze", *map(str, paths)],
        cwd=ROOT, check=True, text=True, capture_output=True)
    return {Path(f["path"]).name: f
            for line in result.stdout.splitlines()
            for f in json.loads(line)["files"]}


def check_traits(label, file, present, absent):
    actual = {t["id"] for t in file.get("traits", [])}
    assert set(present) <= actual, (label, "missing", set(present) - actual)
    assert not set(absent) & actual, (label, "unexpected", set(absent) & actual)
    print("PASS", label)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample", type=Path,
                        help="Optional reviewed managed PE for constant-removal controls")
    args = parser.parse_args()
    cases = json.loads((HERE / "cases.json").read_text())["fixtures"]
    files = scan([ROOT / c["path"] for c in cases])
    for case in cases:
        file = files[Path(case["path"]).name]
        check_traits(case["case_id"], file, case["matched"], case["not_matched"])
        assert all(t["crit"] < 4 for t in file.get("traits", [])), case["case_id"]
    if args.sample:
        original = args.sample.read_bytes()
        variants = [
            ("no-clipboard", "CLIPBOARD:", "CLIPBOARX:", "utf-16le",
             [CLIP], [DEFENDER, LOGON]),
            ("no-keylog", "WH_KEYBOARD_LL", "XX_KEYBOARD_LL", "ascii",
             [CLIP, DEFENDER, LOGON], []),
            ("no-defender", "-DisableRealtimeMonitoring $true",
             "-DisableRealtimeMonitoring $fals", "utf-16le", [DEFENDER], [CLIP, LOGON]),
            ("no-logon", "onlogon", "monthly", "utf-16le", [LOGON], [CLIP, DEFENDER]),
        ]
        # Keep derived executables outside the repository and never execute them.
        with tempfile.TemporaryDirectory() as tmp:
            paths = []
            for name, old, new, encoding, _, _ in variants:
                old, new = old.encode(encoding), new.encode(encoding)
                assert len(old) == len(new) and original.count(old) == 1, name
                path = Path(tmp) / (name + ".exe")
                path.write_bytes(original.replace(old, new))
                paths.append(path)
            files = scan(paths)
            for name, _, _, _, absent, present in variants:
                check_traits(name, files[name + ".exe"], present, absent)


if __name__ == "__main__":
    main()
