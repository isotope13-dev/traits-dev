#!/usr/bin/env python3
"""Run isolated OpAMP exception/credential-signal controls."""
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FIXTURE = Path(__file__).resolve().parent
ID = {
    "opamp": "well-known/lib/network/opentelemetry-opamp::opentelemetry-opamp-client-library",
    "certificate_request": "objectives/lateral-movement/exploit/network-device/provisioning::client-certificate-request",
    "private_key_field": "micro-behaviors/data/parse/vocabulary::private-key-field-name",
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cleave", default=str(ROOT.parent / "cleave/target/release/cleave"))
    parser.add_argument("--traits-dir", default=str(ROOT))
    parser.add_argument("--record", type=Path)
    args = parser.parse_args()
    cases = json.loads((FIXTURE / "cases.json").read_text())
    engine = shutil.which(args.cleave)
    assert engine, f"Cleave not found: {args.cleave}"
    rules = ",".join(cases["rules"])
    records = {}
    with tempfile.TemporaryDirectory(prefix="opamp-control-") as td:
        scratch = Path(td)
        assert "test" not in scratch.name.lower() and "case" not in scratch.name.lower()
        for case in cases["fixtures"]:
            source = FIXTURE / case["path"]
            target = scratch / case["path"]
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
        for case in cases["fixtures"]:
            source = FIXTURE / case["path"]
            target = scratch / case["path"]
            proc = subprocess.run(
                [engine, "--no-update-check", "--traits-dir", str(Path(args.traits_dir).resolve()),
                 "--disable", "yara,radare2,upx", "test-rules", "--rules", rules, str(target)],
                check=True, text=True, capture_output=True,
            )
            output = proc.stdout + proc.stderr
            observed = {
                key: bool(re.search(r"^MATCHED " + re.escape(rid) + r" \(", output, re.M))
                for key, rid in ID.items()
            }
            assert observed == case["expected"], (case["id"], observed, case["expected"], output)
            suppressed = {}
            for key, rid in ID.items():
                if key == "opamp":
                    continue
                block = re.search(
                    r"^NOT MATCHED " + re.escape(rid) + r" \([^\n]*\)(.*?)(?=^MATCHED |^NOT MATCHED |^Summary:)",
                    output, re.M | re.S,
                )
                suppressed[key] = bool(block and "Skipped by 'unless' condition" in block.group(1))
            assert suppressed == case["suppressed"], (case["id"], suppressed, case["suppressed"], output)
            digest = hashlib.sha256(source.read_bytes()).hexdigest()
            records[case["id"]] = {
                "fixture_path": case["path"],
                "sha256": digest,
                "expected_and_observed": observed,
                "unless_suppression_observed": suppressed,
                "note": case["note"],
                "trace": output,
            }
            print(f"{case['id']}: sha256={digest} {observed}")
        if args.record:
            args.record.parent.mkdir(parents=True, exist_ok=True)
            args.record.write_text(json.dumps(records, indent=2, sort_keys=True) + "\n")
    print(f"OpAMP suppressor controls passed: {len(records)} fixtures")


if __name__ == "__main__":
    main()
