#!/usr/bin/env python3
"""Check static findings without executing any sample operations."""
import argparse
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    if args.report:
        output = args.report.read_text()
    else:
        result = subprocess.run(
            [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
             "--format", "json", str(HERE)],
            capture_output=True, text=True)
        # Cleave uses exit 1 when the destruction fixture is detected.
        assert result.returncode in (0, 1), result.stderr
        assert "validation failed" not in result.stdout
        assert "Warning:" not in result.stderr, result.stderr
        output = result.stdout
    findings = {}
    decoder = json.JSONDecoder()
    while output.strip():
        report, end = decoder.raw_decode(output.lstrip())
        output = output.lstrip()[end:]
        for file in report["files"]:
            findings[Path(file["path"]).name] = {
                trait["id"]: trait for trait in file.get("traits", [])}
    checks = 0
    for case in json.loads((HERE / "cases.json").read_text())["fixtures"]:
        found = findings[Path(case["path"]).name]
        for trait in case["matched"]:
            assert trait in found, (case["case_id"], "missing", trait)
            if trait.startswith("objectives/impact/destroy/filesystem::"):
                expected = 4 if trait.endswith("::node-drive-root-truncation-loop") else 5
                assert found[trait]["crit"] == expected, (case["case_id"], found[trait])
            checks += 1
        for trait in case["not_matched"]:
            assert trait not in found, (case["case_id"], "unexpected", trait)
            checks += 1
    print(f"{checks} assertions passed across {len(findings)} analyzed files")


if __name__ == "__main__":
    main()
