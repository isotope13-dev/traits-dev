#!/usr/bin/env python3
"""A settings confirmation is not a model-destructive instruction."""

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
    rule = "objectives/impact/ransom/encrypt/runtime-generated::destructive-data-target-b"
    expected = {"confirmation-ui.js": False, "model-instruction.js": True}

    for name, matched in expected.items():
        with tempfile.TemporaryDirectory(prefix="llm-model-target-") as directory:
            target = Path(directory) / name
            shutil.copyfile(root / "testdata/taxonomy/llm-destructive-model-target" / name, target)
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
