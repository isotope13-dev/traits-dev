#!/usr/bin/env python3
"""Check that embedded shell text is suppressed without hiding a live spawn."""
import argparse
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def reports(text):
    decoder = json.JSONDecoder()
    while text.strip():
        text = text.lstrip()
        value, end = decoder.raw_decode(text)
        yield from value["files"]
        text = text[end:]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cleave",
        default=str(ROOT.parent / "cleave/target/release/cleave"),
        help="Cleave executable (default: sibling ../cleave release binary)",
    )
    args = parser.parse_args()
    cases_path = Path(__file__).with_name("cases.json")
    cases = json.loads(cases_path.read_text())
    cleave = shutil.which(args.cleave)
    assert cleave, f"Missing Cleave executable: {args.cleave}"
    command = [
        str(Path(cleave).resolve()),
        "--no-update-check",
        "--traits-dir",
        str(ROOT),
        "--disable",
        "yara,radare2,upx",
        "--format",
        "json",
        "analyze",
    ]
    env = {**os.environ, "CLEAVE_SKIP_CACHE": "1"}

    with tempfile.TemporaryDirectory(prefix="tax-embedded-shell-") as tmp:
        targets = []
        for case in cases["fixtures"]:
            source = cases_path.parent / case["file"]
            target = Path(tmp) / case["file"]
            shutil.copy2(source, target)
            targets.append(target)

        result = subprocess.run(
            [*command, *map(str, targets)],
            capture_output=True,
            text=True,
            check=True,
            env=env,
        )
        files = {Path(file["path"]).name: file for file in reports(result.stdout)}

        for case in cases["fixtures"]:
            file = files[case["file"]]
            emitted = {trait["id"] for trait in file.get("traits", [])}
            suppressed = {
                entry["id"]
                for entry in file.get("supp", [])
                if entry.get("kind") == "unless"
            }
            suppressors = {
                blocker["id"]
                for entry in file.get("supp", [])
                for blocker in entry.get("by", [])
            }
            operation = cases["operation_rule"]
            assert (cases["embedded_shell_marker"] in suppressors) == case[
                "expect_embedded_shell"
            ], (case["file"], "embedded shell evidence", file)
            if case["expect_embedded_shell"]:
                assert set(cases["suppressed_rules"]) <= suppressed, (
                    case["file"],
                    "expected all five text-level rules to be suppressed",
                    suppressed,
                )
            else:
                assert not set(cases["suppressed_rules"]) & suppressed, (
                    case["file"],
                    "unexpected suppression without embedded shell evidence",
                    suppressed,
                )
            assert (operation in emitted) == case["expect_operation"], (
                case["file"],
                "structured spawn operation",
                emitted,
            )

            print(
                f"PASS {case['file']}: embedded shell "
                f"{'present' if case['expect_embedded_shell'] else 'absent'}, "
                f"spawn operation {'present' if case['expect_operation'] else 'absent'}"
            )


if __name__ == "__main__":
    main()
