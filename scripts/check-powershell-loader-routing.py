#!/usr/bin/env python3
"""Keep neutral PowerShell IEX evidence out of the dropper taxonomy leaf."""

import argparse
from pathlib import Path
import shutil
import subprocess
import tempfile


def main():
    root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cleave", default=str(root.parent / "cleave/target/release/cleave"))
    args = parser.parse_args()

    iex = "micro-behaviors/process/interpreter/eval/direct::powershell-iex-call"
    loader = "objectives/command-and-control/dropper/execution/fileless::curl-custom-ua-piped-powershell"
    cases = {
        "interactive-history.ps1": {iex: True, loader: False},
        "curl-user-agent-piped-iex.ps1": {iex: True, loader: True},
    }
    for name, expected in cases.items():
        with tempfile.TemporaryDirectory(prefix="powershell-loader-") as directory:
            target = Path(directory) / name
            shutil.copyfile(root / "testdata/taxonomy/powershell-loader" / name, target)
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
