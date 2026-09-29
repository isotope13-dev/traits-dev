#!/usr/bin/env python3
"""A generic upload_attachment route is not the Session file server."""

import argparse
from pathlib import Path
import shutil
import subprocess
import tempfile


def run_rules(cleave, root, fixture, rules):
    with tempfile.TemporaryDirectory(prefix="session-fileserver-upload-") as directory:
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

    atom = "objectives/exfiltration/oob/dead-drop::session-attachment-upload-api"
    composite = "objectives/exfiltration/oob/dead-drop::session-fileserver-attachment-upload"
    rules = [atom, composite]

    ordinary = run_rules(
        args.cleave,
        root,
        root / "testdata/taxonomy/session-fileserver-upload/cloudhq-upload.js",
        rules,
    )
    assert_match(ordinary, atom, True, "generic-upload-is-component")
    assert_match(ordinary, composite, False, "generic-upload-not-session-server")

    session = run_rules(
        args.cleave,
        root,
        root / "testdata/taxonomy/session-fileserver-upload/session-upload.js",
        rules,
    )
    assert_match(session, atom, True, "session-upload-verb")
    assert_match(session, composite, True, "session-host-and-upload")


if __name__ == "__main__":
    main()
