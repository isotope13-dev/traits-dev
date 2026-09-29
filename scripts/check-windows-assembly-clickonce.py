#!/usr/bin/env python3
"""A generic Windows assembly namespace is not ClickOnce delivery by itself."""

import argparse
from pathlib import Path
import shutil
import subprocess
import tempfile


def run_rules(cleave, root, fixture, rules):
    with tempfile.TemporaryDirectory(prefix="windows-assembly-clickonce-") as directory:
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

    namespace = "metadata/file/format/markup::windows-assembly-manifest-v2-namespace"
    deployment_url = "objectives/execution/lure/clickonce::clickonce-deploy-url"
    delivery = "objectives/execution/lure/clickonce::clickonce-delivery"
    rules = [namespace, deployment_url, delivery]

    ordinary = run_rules(
        args.cleave,
        root,
        root / "testdata/taxonomy/windows-assembly-manifest/windows-app.manifest",
        rules,
    )
    assert_match(ordinary, namespace, True, "ordinary-assembly-namespace")
    assert_match(ordinary, deployment_url, False, "ordinary-manifest-no-deployment-provider")
    assert_match(ordinary, delivery, False, "ordinary-assembly-not-clickonce")

    clickonce = run_rules(
        args.cleave,
        root,
        root / "testdata/taxonomy/windows-assembly-manifest/clickonce-deployment.manifest",
        rules,
    )
    assert_match(clickonce, namespace, True, "clickonce-assembly-namespace")
    assert_match(clickonce, deployment_url, True, "clickonce-provider-codebase")
    assert_match(clickonce, delivery, True, "clickonce-two-signal-delivery")


if __name__ == "__main__":
    main()
