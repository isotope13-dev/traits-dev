#!/usr/bin/env python3
"""Check browser serialization, instrumentation, and collection boundaries.

Fixtures are scanned, never executed.
"""

import argparse
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
    serializes = "micro-behaviors/data/serialize/json::json-serialization-before-visited-url"
    exports = "objectives/exfiltration/stealer/browser::extension-visited-domain-history-exfil"
    event = "micro-behaviors/os/telemetry/logging/event::file-operation-telemetry-events--read-file-error"
    body = "micro-behaviors/communications/http/services/feishu-lark::feishu-record-body-builder"
    sensitive = "objectives/exfiltration/messaging/webhook::feishu-sensitive-record-content"
    index_miss = "micro-behaviors/data/collection/array::js-allowlist-index-miss"
    empty_miss = "micro-behaviors/data/collection/array::empty-allowlist-index-miss"
    cases = {
        "history-local.js": {serializes: True, exports: False},
        "history-upload.js": {serializes: True, exports: True},
        "feishu-status-only.js": {event: True, body: True, sensitive: False},
        "feishu-key-record.js": {event: True, body: True, sensitive: True},
        "empty-allowlist.js": {index_miss: True, empty_miss: True},
        "populated-allowlist.js": {index_miss: True, empty_miss: False},
    }
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
            shutil.copyfile(root / "testdata/taxonomy/activity-source" / name, target)
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
