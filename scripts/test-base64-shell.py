#!/usr/bin/env python3
"""Scan decode-to-shell controls. Never execute the fixture commands."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
RULE = "micro-behaviors/data/decode/base64::base64-decode-piped-shell"


def main():
    cases = {
        "sh.sh": ("base64 -d | sh", True),
        "bash.sh": ("base64 -D | /bin/bash", True),
        "zsh.sh": ("base64 --decode | /usr/bin/zsh", True),
        "dash.sh": ("base64 -d | env LANG=C /bin/dash", True),
        "env.sh": ("base64 -d | env sh", True),
        "compact.sh": ("base64 -d|ksh", True),
        "input-file.sh": ("base64 -d payload.txt | sh", True),
        "data.sh": ("base64 -d > /tmp/report.txt", False),
        "encode.sh": ("base64 report.txt | sh", False),
        "hash.sh": ("base64 -d | shasum", False),
        "other-command.sh": ("test_base64 -d | sh", False),
        "other-flag.sh": ("base64 -decode | sh", False),
        "separate.sh": ("base64 -d; printf 'echo ok' | sh", False),
        "conditional.sh": ("base64 -d && printf 'echo ok' | sh", False),
    }
    with tempfile.TemporaryDirectory(prefix="base64-shell-controls-") as tmp:
        paths = []
        for name, (command, _) in cases.items():
            path = Path(tmp) / name
            path.write_text("#!/bin/sh\n" + command + "\n")
            paths.append(str(path))
        paths += [
            str(ROOT / "testdata/obfuscation/applescript/base64.scpt"),
            str(ROOT / "testdata/benign/scpt-controls/base64-data.scpt"),
            str(ROOT / "testdata/benign/scpt-controls/profile.scpt"),
        ]
        expected = {name: match for name, (_, match) in cases.items()}
        expected.update({"base64.scpt": True, "base64-data.scpt": False,
                         "profile.scpt": False})
        result = subprocess.run(
            [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
             "--format", "json", *paths],
            cwd=ROOT, capture_output=True, text=True,
            env=dict(os.environ, CLEAVE_SKIP_CACHE="1", FILEFACTS_CACHE="0",
                     CLEAVE_ANALYSIS_MEMO_MB="0", STNG_STRING_CACHE="0"),
            check=True,
        )
        found = {}
        decoder = json.JSONDecoder()
        remaining = result.stdout.lstrip()
        while remaining:
            report, end = decoder.raw_decode(remaining)
            remaining = remaining[end:].lstrip()
            for file in report.get("files", []):
                found[Path(file["path"]).name] = {
                    trait["id"]: trait["crit"] for trait in file.get("traits", [])
                }
        assert found.keys() == expected.keys(), (found.keys(), expected.keys())
        for name, match in expected.items():
            assert (RULE in found[name]) == match, (name, found[name])
            if match:
                assert found[name][RULE] == 4, (name, found[name][RULE])
        for name in ("base64-data.scpt", "profile.scpt"):
            assert all(crit < 4 for crit in found[name].values()), (name, found[name])
        print(f"Passed {len(expected)} static base64 and SCPT controls")


if __name__ == "__main__":
    main()
