#!/usr/bin/env python3
"""Distinguish documented copy syntax from a local FTP build command."""

import argparse
from pathlib import Path
import subprocess


def main():
    root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cleave", default=str(root.parent / "cleave/target/release/cleave"))
    args = parser.parse_args()

    batch = "micro-behaviors/fs/file/copy::cmd-binary-file-concatenation"
    ftp_concat = "micro-behaviors/fs/file/copy::ftp-local-binary-file-concatenation"
    ftp_sequence = "micro-behaviors/communications/ftp/control::ftp-local-shell-command-sequence"
    ftp_launch = "micro-behaviors/process/create/launch::ftp-script-starts-executable"
    ftp_dropper = "objectives/command-and-control/dropper/execution/payload::ftp-script-binary-reconstruction-dropper"
    ftp_decoy = "objectives/evasion/masquerade/document::ftp-script-decoy-payload-launch"

    cases = {
        "manual-example.txt": {batch: False, ftp_concat: False, ftp_dropper: False},
        "build.bat": {batch: True, ftp_concat: False, ftp_dropper: False},
        "ftp-local-build.txt": {
            batch: False,
            ftp_concat: True,
            ftp_sequence: True,
            ftp_launch: True,
            ftp_dropper: True,
            ftp_decoy: True,
        },
    }
    for name, expected in cases.items():
        target = root / "testdata/taxonomy/copy-concat" / name
        result = subprocess.run(
            [args.cleave, "--traits-dir", str(root), "test-rules", "--rules",
             ",".join(expected), str(target)],
            capture_output=True, text=True, check=True,
        )
        output = result.stdout + result.stderr
        for rule, matched in expected.items():
            marker = ("MATCHED " if matched else "NOT MATCHED ") + rule + " "
            if not any(line.startswith(marker) for line in output.splitlines()):
                raise AssertionError(f"{name}: expected {marker.strip()}\n{output}")
        print(f"PASS {name}: {len(expected)} finding assertions", flush=True)


if __name__ == "__main__":
    main()
