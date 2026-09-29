#!/usr/bin/env python3
"""Do not label Pygments filename metadata as credential-file searching."""

import argparse
from pathlib import Path
import shutil
import subprocess
import tempfile


RULE = "objectives/collection/file-targeting/filter::credential-files"


def run_rules(cleave, root, fixture, relative_target):
    with tempfile.TemporaryDirectory(prefix="credential-file-targeting-") as directory:
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
    fixtures = root / "testdata/taxonomy/credential-file-targeting"

    pygments = run_rules(
        args.cleave,
        root,
        fixtures / "pygments-mapping.py",
        Path("site-packages/pipenv/patched/pip/_vendor/pygments/lexers/_mapping.py"),
    )
    assert_match(pygments, False, "pygments-lexer-filename-catalog")

    search = run_rules(
        args.cleave,
        root,
        fixtures / "credential-search.py",
        Path("credential_search.py"),
    )
    assert_match(search, True, "credential-file-search")


if __name__ == "__main__":
    main()
