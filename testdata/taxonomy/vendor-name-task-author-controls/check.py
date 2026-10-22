#!/usr/bin/env python3
"""Preserve task masquerade coverage while placing its neutral atoms correctly."""
import argparse
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
VENDOR = "metadata/vendor/string::javascript-microsoft-corporation-name-reference"
AUTHOR = "micro-behaviors/os/autorun/control::task-author-property-assignment"
ATTACK = "objectives/evasion/masquerade/identity/microsoft::microsoft-author-task-masquerade"
TAIL = "micro-behaviors/data/collection/dom::script-create-near-src-assignment-in-file-tail"
OLD = {
    "objectives/evasion/masquerade/identity/microsoft::microsoft-corporation-author-literal",
    "objectives/evasion/masquerade/identity/microsoft::task-author-property-assignment",
    "micro-behaviors/process/create/load/remote-code::js-dom-script-src-set-in-file-tail",
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cleave", default="cleave")
    args = parser.parse_args()
    cases = {
        "copyright.js": {VENDOR: 3},
        "ordinary-task.js": {AUTHOR: 3},
        "task-masquerade.js": {VENDOR: 3, AUTHOR: 3, ATTACK: 5},
        "analytics-loader.js": {TAIL: 3},
        "script-only.js": {},
        "webpack-loader.js": {},
    }
    targets = [Path(__file__).with_name(name) for name in cases]
    # A separate hostile fixture outside this batch must keep its detection.
    cases["index.js"] = {TAIL: 3}
    targets.append(ROOT / "testdata/hostile/ledger-connect-kit/package/dist/umd/index.js")
    result = subprocess.run(
        [args.cleave, "--traits-dir", str(ROOT), "--format", "json",
         *map(str, targets)],
        capture_output=True, text=True, check=True,
    )
    remaining = result.stdout.lstrip()
    observed = {}
    while remaining:
        report, end = json.JSONDecoder().raw_decode(remaining)
        remaining = remaining[end:].lstrip()
        for file in report["files"]:
            observed[Path(file["path"]).name] = {
                trait["id"]: trait["crit"] for trait in file.get("traits", [])
            }
    for name, expected in cases.items():
        found = observed[name]
        assert not OLD.intersection(found), (name, "misplaced legacy atom")
        selected = {key: value for key, value in found.items()
                    if key in {VENDOR, AUTHOR, ATTACK, TAIL}}
        assert selected == expected, (name, selected, expected)
        print(f"PASS {name}: {selected}")


if __name__ == "__main__":
    main()
