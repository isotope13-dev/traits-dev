#!/usr/bin/env python3
"""Check credential UI, wallet identity references, and process interference.

Fixtures are scanned, never executed.
"""

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile


def main():
    root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cleave", default=str(root.parent / "cleave/target/release/cleave"))
    parser.add_argument("--case", action="append", help="Run only the named fixture (repeatable)")
    args = parser.parse_args()
    cases = json.loads((root / "testdata/taxonomy/wallet-ui/cases.json").read_text())
    if args.case:
        unknown = set(args.case) - cases.keys()
        if unknown:
            parser.error(f"Unknown fixtures: {', '.join(sorted(unknown))}")
        cases = {name: expected for name, expected in cases.items() if name in args.case}
    for name, expected in cases.items():
        # Test-data paths deliberately trigger fixture suppressors. Scan a copy
        # outside that tree so this checks the program's content and source roles.
        with tempfile.TemporaryDirectory(prefix="source-routing-") as directory:
            target = Path(directory) / name
            shutil.copyfile(root / "testdata/taxonomy/wallet-ui" / name, target)
            # Negative broad artifact exclusions make test-rules recursively
            # explain thousands of members. Inspect actual scan findings for
            # these controls instead; this also verifies emitted capabilities.
            if name in {"phantom-activex.js", "tronlink-script.js"}:
                result = subprocess.run(
                    [args.cleave, "--traits-dir", str(root), "--format", "json",
                     "--min-crit", "component", str(target)],
                    capture_output=True, text=True, check=True,
                )
                emitted = {trait["id"] for file in json.loads(result.stdout)["files"]
                           for trait in file.get("traits", [])}
                for rule, matched in expected.items():
                    if (rule in emitted) != matched:
                        raise AssertionError(f"{name}: expected {rule} matched={matched}")
                print(f"PASS {name}: {len(expected)} finding assertions (scan)", flush=True)
                continue
            result = subprocess.run(
                [args.cleave, "--traits-dir", str(root), "test-rules", "--rules",
                 ",".join(expected), str(target)],
                capture_output=True, text=True, check=True,
            )
        output = result.stdout + result.stderr
        for rule, matched in expected.items():
            marker = ("MATCHED " if matched else "NOT MATCHED ") + rule + " "
            if not any(line.startswith(marker) for line in output.splitlines()):
                raise AssertionError(f"{name}: expected {marker.strip()}\n{output}")
        print(f"PASS {name}: {len(expected)} finding assertions", flush=True)


if __name__ == "__main__":
    main()
