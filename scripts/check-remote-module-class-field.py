#!/usr/bin/env python3
"""A generic className mapping is not a remote module descriptor."""

import argparse
from pathlib import Path
import shutil
import subprocess
import tempfile


def run_rules(cleave, root, fixture, rules):
    with tempfile.TemporaryDirectory(prefix="remote-module-class-field-") as directory:
        target = Path(directory) / fixture.name
        shutil.copyfile(fixture, target)
        result = subprocess.run(
            [cleave, "--traits-dir", str(root), "test-rules", "--rules", ",".join(rules), str(target)],
            capture_output=True,
            text=True,
            check=True,
        )
    return result.stdout + result.stderr


def assert_match(output, rule, matched, name):
    marker = ("MATCHED " if matched else "NOT MATCHED ") + rule + " "
    if not any(line.startswith(marker) for line in output.splitlines()):
        raise AssertionError(f"{name}: expected {marker.strip()}\n{output}")
    print(f"PASS {name}: {marker.strip()}", flush=True)


def main():
    root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cleave", default=str(root.parent / "cleave/target/release/cleave"))
    args = parser.parse_args()

    class_field = "objectives/command-and-control/dropper/staged-loader::remote-module-class-field"
    entrypoint = "objectives/command-and-control/dropper/staged-loader::remote-module-entrypoint-fields"
    descriptor = "objectives/command-and-control/dropper/staged-loader::config-driven-remote-module-descriptor"
    rules = [class_field, entrypoint, descriptor]

    ordinary = run_rules(args.cleave, root, root / "testdata/taxonomy/remote-module-class-field/angular-class-name.js", rules)
    assert_match(ordinary, class_field, True, "ordinary-classname-is-component")
    assert_match(ordinary, entrypoint, False, "ordinary-classname-not-entrypoint")
    assert_match(ordinary, descriptor, False, "ordinary-classname-not-loader")

    remote = run_rules(args.cleave, root, root / "testdata/taxonomy/remote-module-class-field/remote-module.json", rules)
    assert_match(remote, class_field, True, "remote-class-field")
    assert_match(remote, entrypoint, True, "remote-class-and-entrypoint")
    assert_match(remote, descriptor, True, "remote-download-integrity-descriptor")


if __name__ == "__main__":
    main()
