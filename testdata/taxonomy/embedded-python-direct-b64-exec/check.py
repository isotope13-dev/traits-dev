#!/usr/bin/env python3
"""Trace direct decode/exec with and without code-shaped string content."""
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
        ",".join((cases["rule"], cases["composite"])),
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

    embedded_case, plain_case = cases["fixtures"]
    embedded_output = outputs[embedded_case["file"]]
    plain_output = outputs[plain_case["file"]]
    rule = cases["rule"]

    # Both fixtures carry the same active decode/exec source line. A separate
    # embedded-code string must not suppress the active AST call.
    assert embedded_case["direct_base64_exec"] == "matched"
    assert plain_case["direct_base64_exec"] == "matched"
    assert cases["decode_exec_line"] in Path(__file__).with_name(
        embedded_case["file"]
    ).read_text()
    assert cases["decode_exec_line"] in Path(__file__).with_name(
        plain_case["file"]
    ).read_text()

    assert f"MATCHED {rule} (trait)" in embedded_output, embedded_output
    assert not any(
        line.startswith(f"NOT MATCHED {rule} (trait)")
        for line in embedded_output.splitlines()
    ), embedded_output
    assert "Found 1 matching AST node(s)" in embedded_output, embedded_output
    assert cases["decode_exec_line"] in embedded_output, embedded_output
    assert f"MATCHED {cases['composite']} (composite)" in embedded_output, embedded_output
    assert f"MATCHED {rule} (trait)" in plain_output, plain_output
    assert not any(
        line.startswith(f"NOT MATCHED {rule} (trait)")
        for line in plain_output.splitlines()
    ), plain_output
    assert f"MATCHED {cases['composite']} (composite)" in plain_output, plain_output

    print(
        f"PASS {embedded_case['file']}: active {rule} remains matched with embedded-code text"
    )
    print(
        f"PASS {plain_case['file']}: {rule} matched the direct decode/exec call"
    )


if __name__ == "__main__":
    main()
