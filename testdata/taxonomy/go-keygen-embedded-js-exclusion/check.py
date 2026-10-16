#!/usr/bin/env python3
"""Build three small Go controls and test the file-wide keygen exclusion."""
import argparse
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = Path(__file__).resolve().parent


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cleave",
        default=str(ROOT.parent / "cleave/target/release/cleave"),
        help="Cleave executable (default: sibling ../cleave release binary)",
    )
    parser.add_argument("--go", default="go", help="Go compiler executable")
    args = parser.parse_args()
    cleave = shutil.which(args.cleave)
    go = shutil.which(args.go)
    assert cleave, f"Missing Cleave executable: {args.cleave}"
    assert go, f"Missing Go compiler: {args.go}"
    cases = json.loads((BASE / "cases.json").read_text())
    env = {**os.environ, "CLEAVE_SKIP_CACHE": "1", "GOWORK": "off"}

    with tempfile.TemporaryDirectory(prefix="tax-go-keygen-") as temp:
        root = Path(temp)
        binaries = []
        for case in cases["fixtures"]:
            binary = root / case["name"]
            subprocess.run(
                [
                    go,
                    "build",
                    "-mod=mod",
                    "-trimpath",
                    "-o",
                    str(binary),
                    "-tags",
                    case["build_tags"],
                    ".",
                ],
                cwd=BASE,
                capture_output=True,
                text=True,
                check=True,
                env=env,
            )
            binaries.append(binary)

        result = subprocess.run(
            [
                cleave,
                "--no-update-check",
                "--traits-dir",
                str(ROOT),
                "--disable",
                "yara,radare2,upx",
                "--format",
                "json",
                "analyze",
                *map(str, binaries),
            ],
            capture_output=True,
            text=True,
            check=True,
            env=env,
        )
        decoder = json.JSONDecoder()
        reports = []
        output = result.stdout.lstrip()
        while output:
            report, end = decoder.raw_decode(output)
            reports.extend(report["files"])
            output = output[end:].lstrip()
        by_name = {Path(file["path"]).name: file for file in reports}

        for case in cases["fixtures"]:
            file = by_name[case["name"]]
            emitted = {trait["id"] for trait in file.get("traits", [])}
            suppressors = {
                blocker["id"]
                for entry in file.get("supp", [])
                for blocker in entry.get("by", [])
            }
            suppressed_rules = {
                entry["id"]
                for entry in file.get("supp", [])
                if entry.get("kind") == "unless"
            }
            keygen = cases["rule"] in emitted
            embedded_js = (
                cases["embedded_javascript"] in emitted
                or cases["embedded_javascript"] in suppressors
            )
            keygen_suppressed_by_js = (
                cases["rule"] in suppressed_rules
                and cases["embedded_javascript"] in suppressors
            )
            assert keygen == case["expect_keygen"], (
                case["name"],
                "key-generation trait mismatch",
                emitted,
                file.get("supp"),
            )
            assert embedded_js == case["expect_embedded_javascript"], (
                case["name"],
                "embedded-JavaScript evidence mismatch",
                emitted,
                file.get("supp"),
            )
            assert keygen_suppressed_by_js == case.get(
                "expect_keygen_suppressed_by_embedded_javascript", False
            ), (
                case["name"],
                "keygen suppression by embedded JavaScript mismatch",
                file.get("supp"),
            )
            print(
                f"{case['name']}: keygen={'present' if keygen else 'absent'}, "
                f"embedded-js={'present' if embedded_js else 'absent'}, "
                f"keygen-suppressed-by-js={'yes' if keygen_suppressed_by_js else 'no'}"
            )


if __name__ == "__main__":
    main()
