#!/usr/bin/env python3
"""Do not mistake pip's script-variant policy comment for payload polymorphism."""

import argparse
from pathlib import Path
import shutil
import subprocess
import tempfile


RULE = "objectives/anti-static/obfuscation/payload/polymorphic::variant-generation-verb"


def run_rules(cleave, root, fixture, relative_target):
    with tempfile.TemporaryDirectory(prefix="variant-generation-context-") as directory:
        target = Path(directory) / relative_target
        target.parent.mkdir(parents=True, exist_ok=True)
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
    fixtures = root / "testdata/taxonomy/polymorphic-variant-context"

    pip_source = run_rules(
        args.cleave,
        root,
        fixtures / "pip-wheel.py",
        Path("pip/operations/install/wheel.py"),
    )
    assert_match(pip_source, False, "pip-script-variant-policy")

    payload = run_rules(args.cleave, root, fixtures / "payload.py", Path("payload.py"))
    assert_match(payload, True, "payload-variant-generation")


if __name__ == "__main__":
    main()
