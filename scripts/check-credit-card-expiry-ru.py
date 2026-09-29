#!/usr/bin/env python3
"""Russian subscription-expiry prose is not a credit-card field."""

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
    rule = "objectives/credential-access/financial/credit-card/form-field::expiry-field-ru"
    expected = {"subscription-expired.js": False, "card-expiry-label.js": True}

    for name, matched in expected.items():
        with tempfile.TemporaryDirectory(prefix="expiry-ru-") as directory:
            target = Path(directory) / name
            shutil.copyfile(root / "testdata/taxonomy/credit-card-expiry-ru" / name, target)
            result = subprocess.run(
                [args.cleave, "--traits-dir", str(root), "test-rules", "--rules", rule, str(target)],
                capture_output=True,
                text=True,
                check=True,
            )
        marker = ("MATCHED " if matched else "NOT MATCHED ") + rule + " "
        output = result.stdout + result.stderr
        if not any(line.startswith(marker) for line in output.splitlines()):
            raise AssertionError(f"{name}: expected {marker.strip()}\n{output}")
        print(f"PASS {name}: {marker.strip()}", flush=True)


if __name__ == "__main__":
    main()
