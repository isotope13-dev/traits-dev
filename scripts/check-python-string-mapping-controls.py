#!/usr/bin/env python3
"""Keep generic Python character mapping distinct from ROT13."""

import argparse
from pathlib import Path
import shutil
import subprocess
import tempfile


GENERIC = "micro-behaviors/data/string/mutate::python-maketrans-table"
ROT13 = "micro-behaviors/data/encode/rot13::python-rot13-decoder"
BASE64_LITERAL = "metadata/file/encoded::python-long-base64-looking-string-literal"
AI_TASK = "micro-behaviors/communications/http/url/query::ai-prompt-query-key-basic"
PHP_ENDPOINT = "micro-behaviors/communications/http/url/php-endpoint::url-php-endpoint-script"


def run_rules(cleave, root, rule, fixture):
    with tempfile.TemporaryDirectory(prefix="python-string-mapping-") as directory:
        target = Path(directory) / fixture.name
        shutil.copyfile(fixture, target)
        result = subprocess.run(
            [cleave, "--traits-dir", str(root), "test-rules", "--rules", rule, str(target)],
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
    fixtures = root / "testdata/taxonomy/python-string-mapping"

    generic = fixtures / "generic.py"
    assert_match(run_rules(args.cleave, root, GENERIC, generic), GENERIC, True, "generic-mapping")
    assert_match(run_rules(args.cleave, root, ROT13, generic), ROT13, False, "generic-is-not-rot13")

    rot13 = fixtures / "rot13.py"
    assert_match(run_rules(args.cleave, root, ROT13, rot13), ROT13, True, "rot13-mapping")

    camelcase = fixtures / "camelcase.py"
    assert_match(
        run_rules(args.cleave, root, BASE64_LITERAL, camelcase),
        BASE64_LITERAL,
        False,
        "camel-case-country-keys-are-not-base64",
    )
    padded = fixtures / "base64.py"
    assert_match(
        run_rules(args.cleave, root, BASE64_LITERAL, padded),
        BASE64_LITERAL,
        True,
        "base64-literal-content",
    )

    cms = fixtures / "cms-download-task.py"
    assert_match(run_rules(args.cleave, root, AI_TASK, cms), AI_TASK, False, "cms-download-task")
    prompt = fixtures / "prompt-query.py"
    assert_match(run_rules(args.cleave, root, AI_TASK, prompt), AI_TASK, True, "prompt-query")

    archived = fixtures / "archived-php-url.py"
    assert_match(
        run_rules(args.cleave, root, PHP_ENDPOINT, archived),
        PHP_ENDPOINT,
        False,
        "archive-wraps-inner-php-path",
    )
    direct = fixtures / "direct-php-url.py"
    assert_match(
        run_rules(args.cleave, root, PHP_ENDPOINT, direct),
        PHP_ENDPOINT,
        True,
        "direct-php-endpoint",
    )


if __name__ == "__main__":
    main()
