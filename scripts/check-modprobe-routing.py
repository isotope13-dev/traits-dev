#!/usr/bin/env python3
"""Keep modprobe persistence evidence separate from pip's similar option."""

import argparse
from pathlib import Path
import subprocess


def main():
    root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cleave", default=str(root.parent / "cleave/target/release/cleave"))
    args = parser.parse_args()

    flag = "micro-behaviors/os/kernel/module::modprobe-ignore-install-flag"
    directive = "micro-behaviors/os/kernel/module::modprobe-install-command-line"
    config_path = "micro-behaviors/os/kernel/module::modprobe-config-path"
    chain = "micro-behaviors/os/kernel/module::modprobe-shell-metachar"
    hook = "objectives/persistence/system/surface/modprobe::modprobe-install-hook"

    cases = {
        "pip-ignore-installed.py": {flag: False, hook: False},
        "example.conf": {directive: True, flag: True, config_path: False, hook: False},
        "etc/modprobe.d/override.conf": {
            directive: True,
            flag: True,
            config_path: True,
            chain: False,
            hook: True,
        },
    }
    for name, expected in cases.items():
        target = root / "testdata/taxonomy/modprobe" / name
        result = subprocess.run(
            [
                args.cleave,
                "--traits-dir",
                str(root),
                "test-rules",
                "--rules",
                ",".join(expected),
                str(target),
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        output = result.stdout + result.stderr
        for rule, matched in expected.items():
            marker = ("MATCHED " if matched else "NOT MATCHED ") + rule + " "
            if not any(line.startswith(marker) for line in output.splitlines()):
                raise AssertionError(f"{name}: expected {marker.strip()}\n{output}")
        print(f"PASS {name}: {len(expected)} finding assertions", flush=True)


if __name__ == "__main__":
    main()
