#!/usr/bin/env python3
"""Check that generic Scapy provenance cannot suppress the PE hook."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CASES = Path(__file__).with_name("cases.json")
HOOK = "objectives/anti-analysis/anti-tampering/archive::builtin-binary-embedded-base64-pe"
CONTEXT = "embedded-base64-compressed-test-fixture-context"
SKIP = f'Skipped by \'unless\' condition: Trait {{ id: "{CONTEXT}" }}'


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cleave", default=str(ROOT.parent / "cleave/target/release/cleave"))
    args = parser.parse_args()

    with tempfile.TemporaryDirectory(prefix="scapy-controls-") as tmp:
        record = Path(tmp) / "findings.json"
        subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/check-taxonomy-cases.py"),
                "--cleave",
                args.cleave,
                "--cases",
                str(CASES),
                "--record",
                str(record),
            ],
            cwd=ROOT,
            check=True,
        )
        traces = json.loads(record.with_suffix(".traces.json").read_text())

    generic = traces["generic-header-alone-does-not-suppress"]
    split = traces["utscapy-markers-split-across-members-do-not-suppress"]
    authentic = traces["complete-utscapy-source-marker-conjunction"]
    assert f"MATCHED {HOOK} (trait)" in generic, "generic-header control must match the PE hook"
    assert SKIP not in generic, "generic Scapy header must not trigger the fixture-context exception"
    assert f"MATCHED {HOOK} (trait)" in split, "split-marker control must match the PE hook"
    assert SKIP not in split, "markers from separate members must not trigger the fixture-context exception"
    assert SKIP in authentic, "complete UTscapy source markers must trigger the fixture-context exception"
    print("Scapy suppressor checks passed: generic/split markers leave the PE hook active; UTscapy source context suppresses it")


if __name__ == "__main__":
    main()
