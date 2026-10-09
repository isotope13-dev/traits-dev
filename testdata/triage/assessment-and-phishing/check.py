#!/usr/bin/env python3
"""Check source/template boundaries without executing any fixture."""
import json
import pathlib
import shutil
import subprocess
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
EXPECTED = {
    "active-shell.py": (1, None),
    "plugin-with-activation.py": (1, None),
    "template-shell.py": (0, 0),
    "browser-artwork.ts": (0, 0),
    "ordinary-auth.ts": (0, 0),
    "endianness.py": (0, 0),
    "credential-export.ts": (3, 1),
}
with tempfile.TemporaryDirectory(prefix="assessment-controls-") as directory:
    for name in EXPECTED:
        shutil.copyfile(HERE / name, pathlib.Path(directory) / name)
    result = subprocess.run(
        ["atomscan", "--no-update", "--mode", "slow", "-f", "json", directory],
        capture_output=True, text=True,
    )
    if not result.stdout.strip():
        raise SystemExit(result.stderr or "No scan results")
    actual = {}
    for line in result.stdout.splitlines():
        report = json.loads(line)
        for item in report["raw"]["files"]:
            name = pathlib.Path(item["path"]).name
            if name not in EXPECTED:
                continue
            traits = item.get("traits", [])
            hostile = {t["id"] for t in traits if t["crit"] == 5}
            suspicious = {t["id"] for t in traits if t["crit"] == 4}
            actual[name] = (len(hostile), len(suspicious))
    for name, (expected_hostile, expected_suspicious) in EXPECTED.items():
        hostile, suspicious = actual[name]
        if expected_suspicious is None:
            assert hostile >= expected_hostile, (name, actual[name])
        else:
            assert (hostile, suspicious) == (expected_hostile, expected_suspicious), (
                name, actual[name], EXPECTED[name]
            )
        print(f"PASS {name}: {hostile} hostile, {suspicious} suspicious")
