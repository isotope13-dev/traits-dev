#!/usr/bin/env python3
"""Keep string-replacement obfuscation separate from computed methods."""

import argparse
from pathlib import Path
import subprocess


def main():
    root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cleave", default=str(root.parent / "cleave/target/release/cleave"))
    args = parser.parse_args()

    replace = "objectives/anti-static/obfuscation/string/recovery::js-bracket-replace-call"
    deobfuscation = "objectives/anti-static/obfuscation/string/recovery::js-token-substitution-deobfuscation"
    cases = {
        "token-substitution.js": {replace: True, deobfuscation: True},
        "computed-private-methods.js": {replace: False, deobfuscation: False},
    }
    fixtures = root / "testdata/taxonomy/string-recovery"
    for name, expected in cases.items():
        result = subprocess.run(
            [args.cleave, "--traits-dir", str(root), "test-rules", "--rules",
             ",".join(expected), str(fixtures / name)],
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
