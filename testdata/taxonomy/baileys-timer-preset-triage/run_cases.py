#!/usr/bin/env python3
"""Run the baileys-timer-preset-triage fixtures against cleave."""

import argparse
import json
import subprocess
import tempfile
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cleave", default="cleave")
    args = parser.parse_args()
    cases = json.loads((HERE / "cases.json").read_text())["cases"]

    failures = []
    for case in cases:
        source = HERE / case["path"]
        # Run outside testdata so test-directory context does not suppress
        # findings that these specimens are intended to exercise.
        with tempfile.TemporaryDirectory(prefix="baileys-triage-") as td:
            target = Path(td) / source.name
            target.write_bytes(source.read_bytes())
            if case["command"] == "analyze":
                cmd = [args.cleave, "--traits-dir", str(REPO), "--format", "json", "analyze", str(target)]
                result = subprocess.run(cmd, text=True, capture_output=True)
                if result.returncode:
                    failures.append(f"{source.name}: analyze failed: {result.stderr.strip()}")
                    continue
                report = json.loads(result.stdout)
                findings = {trait["id"] for row in report["files"] for trait in row.get("traits", [])}
                missing = [item for item in case["must_match"] if not any(item == found or found.startswith(item) for found in findings)]
                unexpected = [item for item in case["must_not_match"] if any(item == found or found.startswith(item) for found in findings)]
                if missing or unexpected:
                    failures.append(f"{source.name}: missing={missing}; unexpected={unexpected}")
            elif case["command"] == "test-rules":
                cmd = [args.cleave, "--traits-dir", str(REPO), "test-rules", "--rules", case["rule"], str(target)]
                result = subprocess.run(cmd, text=True, capture_output=True)
                output = result.stdout + result.stderr
                if result.returncode:
                    failures.append(f"{source.name}: test-rules failed: {output.strip()}")
                    continue
                status = "matched" if f"MATCHED {case['rule']}" in output and f"NOT MATCHED {case['rule']}" not in output else "not matched"
                absent = [needle for needle in case.get("must_contain", []) if needle not in output]
                present = [needle for needle in case.get("must_not_contain", []) if needle in output]
                if status != case["expect"] or absent or present:
                    failures.append(f"{source.name}: expected {case['expect']}, got {status}; missing text={absent}; forbidden text={present}\n{output.strip()}")
            else:
                failures.append(f"{source.name}: unknown command {case['command']!r}")

    if failures:
        print("baileys timer-preset triage failures:")
        print("\n".join(f"- {failure}" for failure in failures))
        return 1
    print(f"baileys timer-preset triage ok: {len(cases)} cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
