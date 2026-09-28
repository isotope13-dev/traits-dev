#!/usr/bin/env python3
"""Check browser history source, storage, and helper boundaries.

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
    storage = "micro-behaviors/data/db/web-storage::browser-local-storage-interfaces"
    export = "objectives/exfiltration/stealer/browser::extension-visited-domain-history-exfil"
    observed_send = "objectives/exfiltration/stealer/browser::extension-request-host-upload"
    tabs = "objectives/exfiltration/stealer/browser::extension-tab-visited-url-exfil"
    helper = "micro-behaviors/communications/http/cookie-store::recognized-minified-cookie-helper-functions"
    identity = "well-known/tool/development/docs/haddock::recognized-haddock-style-cookie-helper"
    theft = "objectives/exfiltration/messaging/webhook::discord-exfiltration"
    cases = {
        "storage-upload.js": {storage: True, export: True, observed_send: True},
        "crypto-upload.js": {storage: False, export: False, observed_send: True},
        "direct-body-upload.js": {storage: True, export: True, observed_send: True},
        "tab-upload.js": {storage: True, tabs: True},
        "tab-distant-request.js": {storage: True, tabs: False},
        "recognized-cookie-helper.js": {helper: True, identity: True, theft: False},
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
            shutil.copyfile(root / "testdata/taxonomy/browser-history" / name, target)
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
