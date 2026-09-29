#!/usr/bin/env python3
"""Stock UPX compression must not be escalated to suspicious or hostile."""

import json
import os
from pathlib import Path
import shutil
import subprocess


EXPECTED_NOTABLE = {
    "anti-static/packer/upx",
    "objectives/anti-static/pack/upx::upx-sectionless-high-entropy-elf",
    "objectives/anti-static/pack/upx::upx-static-sectionless-banner-elf",
}


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    sample = root / "testdata/benign/zapret-tpws-v72.9"
    if shutil.which("upx") is None:
        raise SystemExit("UPX is required to verify the unpacked stock-UPX path")

    env = os.environ.copy()
    env["CLEAVE_TRAITS_DIR"] = str(root)
    result = subprocess.run(
        [
            "atomscan",
            "--no-update",
            "--mode",
            "slow",
            "--format",
            "json",
            "path",
            str(sample),
        ],
        capture_output=True,
        text=True,
        check=True,
        env=env,
    )
    rows = [json.loads(line) for line in result.stdout.splitlines() if line.strip()]
    file_row = next(
        file
        for row in rows
        for file in row["raw"]["files"]
        if file["path"] == str(sample)
    )
    traits = {trait["id"]: trait for trait in file_row["traits"]}

    missing = EXPECTED_NOTABLE - traits.keys()
    if missing:
        raise AssertionError(f"expected stock UPX observations are absent: {sorted(missing)}")
    elevated = [trait for trait in traits.values() if trait["crit"] >= 4]
    if elevated:
        raise AssertionError(
            "stock UPX compression produced suspicious/hostile findings: "
            + ", ".join(trait["id"] for trait in elevated)
        )
    wrong_levels = [
        trait["id"]
        for trait in traits.values()
        if trait["id"] in EXPECTED_NOTABLE and trait["crit"] != 3
    ]
    if wrong_levels:
        raise AssertionError(f"stock UPX observations must remain notable: {wrong_levels}")

    print("PASS stock UPX ELF packing remains notable after successful unpacking")


if __name__ == "__main__":
    main()
