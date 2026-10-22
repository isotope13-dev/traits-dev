#!/usr/bin/env python3
"""Run the source/constructor boundary controls against the local rules."""
import argparse
import json
from pathlib import Path
import subprocess


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cleave", default="cleave")
    parser.add_argument("--record", type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[3]
    cases = json.loads(Path(__file__).with_name("cases.json").read_text())["fixtures"]
    results = []
    for case in cases:
        proc = subprocess.run(
            [args.cleave, "--traits-dir", str(root), "--format", "json", str(root / case["path"])],
            text=True, capture_output=True, check=True,
        )
        report = json.loads(proc.stdout)
        matched = {t["id"] for f in report["files"] for t in f.get("traits", [])}
        missing = set(case["matched"]) - matched
        unexpected = set(case["not_matched"]) & matched
        assert not missing and not unexpected, (case["case_id"], missing, unexpected)
        results.append({"case": case["case_id"], "passed": True})
        print(f"PASS {case['case_id']}")
    if args.record:
        args.record.write_text(json.dumps(results, indent=2) + "\n")


if __name__ == "__main__":
    main()
