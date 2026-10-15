#!/usr/bin/env python3
"""Pin the embedded-Python exclusion on direct-base64-exec with test-rules."""
import argparse
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


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
        "test-rules",
        "--rules",
        cases["rule"],
    ]
    env = {**os.environ, "CLEAVE_SKIP_CACHE": "1"}

    with tempfile.TemporaryDirectory(prefix="tax-") as tmp:
        assert not any(word in Path(tmp).name.lower() for word in ("test", "case"))
        for case in cases["fixtures"]:
            source = cases_path.parent / case["file"]
            target = Path(tmp) / case["file"]
            shutil.copy2(source, target)
            result = subprocess.run(
                [*command, str(target)],
                capture_output=True,
                text=True,
                check=True,
                env=env,
            )
            output = result.stdout + result.stderr
            rule = cases["rule"]
            matched = any(
                line.startswith(f"MATCHED {rule} (trait)")
                for line in output.splitlines()
            )
            not_matched = any(
                line.startswith(f"NOT MATCHED {rule} (trait)")
                for line in output.splitlines()
            )
            if case["direct_base64_exec"] == "present":
                assert matched and not not_matched, output
            else:
                assert not_matched and not matched, output

            marker = cases["embedded_python_marker"]
            suppressed_by = case["suppressed_by"]
            if suppressed_by:
                expected = (
                    "Skipped by 'unless' condition: Trait { id: "
                    f'"{suppressed_by}" }} [matched: {suppressed_by}]'
                )
                assert expected in output, output
                assert marker == suppressed_by
            else:
                assert marker not in output, output
            print(f"PASS {case['file']}: direct-base64-exec {case['direct_base64_exec']}")


if __name__ == "__main__":
    main()
