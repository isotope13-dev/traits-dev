#!/usr/bin/env python3
"""Check the reverse-engineered DOS COM overwriter and benign controls."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPECIMEN_SHA256 = "d5cb77880c6cc5d9c05df276ee35d4b273ad85a6f5702126544316066998ebb1"
HOSTILE = "objectives/impact/infect/binary/dos/com-bytes::dos-com-first-match-overwriter"


def traits(binary: str, path: Path) -> dict[str, int]:
    result = subprocess.run(
        [binary, "--traits-dir", str(ROOT), "--format", "json", str(path)],
        capture_output=True,
        text=True,
        check=True,
    )
    report = json.loads(result.stdout)
    return {
        trait["id"]: trait["crit"]
        for file in report["files"]
        for trait in file.get("traits", [])
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cleave", default="cleave")
    args = parser.parse_args()

    sample = ROOT / "testdata/hostile/dos-com/anton-97"
    digest = hashlib.sha256(sample.read_bytes()).hexdigest()
    assert digest == SPECIMEN_SHA256, f"specimen fixture changed: {digest}"
    matched = traits(args.cleave, sample)
    assert matched.get(HOSTILE, 0) >= 5, ("missing overwrite finding", matched)
    print("anton-97: passed", flush=True)

    for name in ("dos-table-query.com", "dos-ah52-unrelated-call.com"):
        control = ROOT / "testdata/benign" / name
        matched = traits(args.cleave, control)
        assert HOSTILE not in matched, (name, "benign DOS utility matched", matched)
        print(f"{name}: passed", flush=True)


if __name__ == "__main__":
    main()
