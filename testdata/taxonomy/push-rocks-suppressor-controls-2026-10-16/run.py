#!/usr/bin/env python3
"""Run bounded same-file controls for the declared push.rocks suppressor edges."""
import argparse
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FIXTURE = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cleave", default=str(ROOT.parent / "cleave/target/release/cleave"))
    parser.add_argument("--traits-dir", default=str(ROOT))
    parser.add_argument("--record", type=Path)
    args = parser.parse_args()
    cases = json.loads((FIXTURE / "cases.json").read_text())
    engine = shutil.which(args.cleave)
    assert engine, f"Cleave not found: {args.cleave}"
    records = {}
    for case in cases["fixtures"]:
        path = FIXTURE / case["path"]
        target = case["target"]
        suppressor = case["suppressor"]
        proc = subprocess.run(
            [engine, "--no-update-check", "--traits-dir", str(Path(args.traits_dir).resolve()),
             "--disable", "yara,radare2,upx", "test-rules", "--rules",
             f"{target},{suppressor}", str(path)],
            check=True, text=True, capture_output=True,
        )
        output = proc.stdout + proc.stderr
        matched = bool(re.search(r"^MATCHED " + re.escape(target) + r" \(", output, re.M))
        suppressed = bool(re.search(
            r"^NOT MATCHED " + re.escape(target) + r" \([^\n]*\)(.*?)(?=^MATCHED |^NOT MATCHED |^Summary:)",
            output, re.M | re.S,
        ) and "Skipped by 'unless' condition" in re.search(
            r"^NOT MATCHED " + re.escape(target) + r" \([^\n]*\)(.*?)(?=^MATCHED |^NOT MATCHED |^Summary:)",
            output, re.M | re.S,
        ).group(1))
        marker_matched = bool(re.search(r"^MATCHED " + re.escape(suppressor) + r" \(", output, re.M))
        observed = {"target_match": matched, "suppressor_match": marker_matched, "suppression": suppressed}
        expected = {"target_match": case["target_match"], "suppression": case["suppression"]}
        assert matched == case["target_match"], (case["id"], observed, expected, output)
        assert suppressed == case["suppression"], (case["id"], observed, expected, output)
        # A suppressor may still match after its `unless` edge is removed. The
        # property under test is whether that match suppresses the target.
        assert not suppressed or marker_matched, (case["id"], observed, expected, output)
        records[case["id"]] = {
            "fixture_path": case["path"],
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "target": target,
            "suppressor": suppressor,
            "expected_and_observed": observed,
            "note": case["note"],
            "trace": output,
        }
        print(f"{case['id']}: sha256={records[case['id']]['sha256']} {observed}")
    if args.record:
        args.record.parent.mkdir(parents=True, exist_ok=True)
        args.record.write_text(json.dumps(records, indent=2, sort_keys=True) + "\n")
    print(f"push.rocks suppressor controls passed: {len(records)} fixtures")


if __name__ == "__main__":
    main()
