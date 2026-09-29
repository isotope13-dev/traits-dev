#!/usr/bin/env python3
"""Keep generic buffer copies distinct from WSH FileObject copy calls."""

import argparse
from pathlib import Path
import shutil
import subprocess
import tempfile


RULE = "objectives/impact/infect/script/self-copy::wsh-file-copy-call"


def run_rules(cleave, root, fixture):
    with tempfile.TemporaryDirectory(prefix="wsh-file-copy-") as directory:
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
    fixtures = root / "testdata/taxonomy/wsh-file-copy-matcher"

    assert_match(run_rules(args.cleave, root, fixtures / "buffer-copy.js"), False, "generic-buffer-copy")
    assert_match(run_rules(args.cleave, root, fixtures / "wsh-copy.js"), True, "wsh-fileobject-copy")


if __name__ == "__main__":
    main()
