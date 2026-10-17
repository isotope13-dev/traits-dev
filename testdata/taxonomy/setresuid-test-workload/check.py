#!/usr/bin/env python3
"""Check that a syscall test workload does not convict as setresuid co-occurrence."""
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

    with tempfile.TemporaryDirectory(prefix="tax-setresuid-") as tmp:
        targets = []
        for case in cases["fixtures"]:
            source = cases_path.parent / case["file"]
            target = Path(tmp) / case["file"]
            target.parent.mkdir(parents=True, exist_ok=True)
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
            file = files[Path(case["file"]).name]
            emitted = {trait["id"] for trait in file.get("traits", [])}
            assert (cases["profile_rule"] in emitted) == case[
                "expect_profile"
            ], (case["file"], "setresuid co-occurrence", file)
            assert (cases["atom_rule"] in emitted) == case["expect_atom"], (
                case["file"],
                "setresuid root atom",
                file,
            )
            print(
                f"PASS {case['file']}: neutral profile "
                f"{'present' if case['expect_profile'] else 'absent'}, "
                f"atom {'present' if case['expect_atom'] else 'absent'}"
            )


if __name__ == "__main__":
    main()
