#!/usr/bin/env python3
"""Trace the embedded-Python exclusion and retained direct-call control."""
import argparse
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def run_case(cleave: str, cases: dict, case: dict, temp_root: Path) -> str:
    source = Path(__file__).with_name(case["file"])
    target = temp_root / case["file"]
    shutil.copy2(source, target)
    command = [
        cleave,
        "--no-update-check",
        "--traits-dir",
        str(ROOT),
        "--disable",
        "yara,radare2,upx",
        "test-rules",
        "--rules",
        cases["rule"],
        str(target),
    ]
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=True,
        env={**os.environ, "CLEAVE_SKIP_CACHE": "1"},
    )
    return result.stdout + result.stderr


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cleave",
        default=str(ROOT.parent / "cleave/target/release/cleave"),
        help="Cleave executable (default: sibling ../cleave release binary)",
    )
    args = parser.parse_args()
    cleave = shutil.which(args.cleave)
    assert cleave, f"Missing Cleave executable: {args.cleave}"
    cases = json.loads(Path(__file__).with_name("cases.json").read_text())
    outputs = {}

    with tempfile.TemporaryDirectory(prefix="tax-embed-b64-") as tmp:
        temp_root = Path(tmp)
        assert not any(word in temp_root.name.lower() for word in ("test", "case"))
        for case in cases["fixtures"]:
            outputs[case["file"]] = run_case(cleave, cases, case, temp_root)

    suppressed_case, retained_case = cases["fixtures"]
    suppressed_output = outputs[suppressed_case["file"]]
    retained_output = outputs[retained_case["file"]]
    rule = cases["rule"]
    marker = cases["embedded_python_marker"]

    # Both fixtures carry the exact same active decode/exec source line. The
    # retained trace proves that line satisfies the rule's AST matcher; the
    # paired trace proves the embedded-language finding suppresses it.
    assert suppressed_case["direct_base64_exec"] == "suppressed"
    assert retained_case["direct_base64_exec"] == "retained"
    assert cases["decode_exec_line"] in Path(__file__).with_name(
        suppressed_case["file"]
    ).read_text()
    assert cases["decode_exec_line"] in Path(__file__).with_name(
        retained_case["file"]
    ).read_text()

    assert f"NOT MATCHED {rule} (trait)" in suppressed_output, suppressed_output
    assert not any(
        line.startswith(f"MATCHED {rule} (trait)")
        for line in suppressed_output.splitlines()
    ), suppressed_output
    expected_skip = (
        "Skipped by 'unless' condition: Trait { id: "
        f'"{marker}" }} [matched: {marker}]'
    )
    assert expected_skip in suppressed_output, suppressed_output

    assert f"MATCHED {rule} (trait)" in retained_output, retained_output
    assert not any(
        line.startswith(f"NOT MATCHED {rule} (trait)")
        for line in retained_output.splitlines()
    ), retained_output
    assert "Found 1 matching AST node(s)" in retained_output, retained_output
    assert cases["decode_exec_line"] in retained_output, retained_output
    assert marker not in retained_output, retained_output

    print(
        f"PASS {suppressed_case['file']}: {rule} suppressed by matched {marker}"
    )
    print(
        f"PASS {retained_case['file']}: {rule} matched the same direct decode/exec call"
    )


if __name__ == "__main__":
    main()
