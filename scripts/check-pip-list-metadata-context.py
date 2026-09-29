#!/usr/bin/env python3
"""Keep the Python package-list signal distinct from runtime-version lookup."""

import argparse
from pathlib import Path
import shutil
import subprocess
import tempfile


RULE = "objectives/supply-chain/install-hook/package/wheel-sdist::python-pip-list-metadata"


def run_rules(cleave, root, fixture):
    with tempfile.TemporaryDirectory(prefix="pip-list-metadata-") as directory:
        target = Path(directory) / fixture.name
        shutil.copyfile(fixture, target)
        result = subprocess.run(
            [cleave, "--traits-dir", str(root), "test-rules", "--rules", RULE, str(target)],
            capture_output=True,
            text=True,
            check=True,
        )
    return result.stdout + result.stderr


def assert_match(output, matched, name):
    marker = ("MATCHED " if matched else "NOT MATCHED ") + RULE + " "
    if not any(line.startswith(marker) for line in output.splitlines()):
        raise AssertionError(f"{name}: expected {marker.strip()}\n{output}")
    print(f"PASS {name}: {marker.strip()}", flush=True)


def main():
    root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cleave", default=str(root.parent / "cleave/target/release/cleave"))
    args = parser.parse_args()

    fixtures = root / "testdata/taxonomy/pip-list-metadata"
    assert_match(
        run_rules(args.cleave, root, fixtures / "pip-package-list.py"),
        True,
        "pip-package-inventory",
    )
    assert_match(
        run_rules(args.cleave, root, fixtures / "pymanager-runtime-list.py"),
        False,
        "pymanager-runtime-availability",
    )


if __name__ == "__main__":
    main()
