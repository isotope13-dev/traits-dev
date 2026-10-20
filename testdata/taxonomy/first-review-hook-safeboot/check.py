#!/usr/bin/env python3
"""Check hook, recovery-administration and function-population boundaries."""
import argparse
import json
from pathlib import Path
import subprocess


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cleave", default="cleave")
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    root = here.parents[2]
    cases = json.loads((here / "cases.json").read_text())["fixtures"]
    for case in cases:
        result = subprocess.run(
            [args.cleave, "--traits-dir", str(root), "--format", "json",
             str(root / case["path"])],
            capture_output=True, text=True, check=True,
        )
        report = json.loads(result.stdout)
        traits = [t for f in report["files"] for t in f["traits"]]
        ids = {t["id"] for t in traits}
        missing = set(case["matched"]) - ids
        unexpected = set(case["not_matched"]) & ids
        hostile = [t["id"] for t in traits if t["crit"] == 5]
        assert not (missing or unexpected or hostile), (
            case["case_id"], missing, unexpected, hostile
        )
        print("PASS", case["case_id"])


if __name__ == "__main__":
    main()
