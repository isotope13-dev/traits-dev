#!/usr/bin/env python3
"""Check the malcontent exception against its upstream identity constants."""

import argparse
from pathlib import Path
import subprocess
import tempfile


def main():
    root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cleave", default=str(root.parent / "cleave/target/release/cleave"))
    parser.add_argument("--cc", default="cc")
    args = parser.parse_args()

    project = "well-known/tool/detection/malcontent::malcontent-project-marker"
    catalog = "well-known/tool/detection/malcontent::malcontent-yara-catalog"
    upx_key = "well-known/tool/detection/malcontent::malcontent-upx-config-key"
    exception = "well-known/tool/detection/malcontent::malcontent-defensive-scanner-context"
    cases = {
        "scanner.c": {project: True, catalog: True, upx_key: True, exception: True},
        "missing-upx-key.c": {project: True, catalog: True, upx_key: False, exception: False},
        "missing-project.c": {project: False, catalog: True, upx_key: True, exception: False},
    }
    fixtures = root / "testdata/taxonomy/malcontent"
    for name, expected in cases.items():
        with tempfile.TemporaryDirectory(prefix="malcontent-exception-") as directory:
            target = Path(directory) / "fixture"
            subprocess.run(
                [args.cc, str(fixtures / name), "-o", str(target)], check=True,
                capture_output=True, text=True,
            )
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
