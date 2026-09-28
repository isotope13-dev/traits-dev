#!/usr/bin/env python3
"""Check browser locator, protection mechanism, and consumer boundaries.

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
    client = "objectives/exfiltration/stealer/browser::js-browser-stealer-c2"
    path = "micro-behaviors/fs/path/application/browser::chrome-path"
    cdp = "objectives/credential-access/browser/devtools::chromium-cdp-live-storage-cookie-harvest"
    app_bound = "objectives/credential-access/browser/app-bound::chromium-app-bound-key-name"
    output = "objectives/credential-access/browser/loot::appbound-key-artifact"
    defanged = "micro-behaviors/communications/ip/parse::defanged-ip-delimited-dots"
    cases = {
        "defanged-public.js": {defanged: True, client: False},
        "defanged-private.js": {defanged: True, client: False},
        "defanged-invalid.js": {defanged: False, client: False},
        "path-client.js": {path: True, client: False},
        "devtools-client.js": {cdp: True, client: True},
        "devtools-no-client.js": {cdp: True, client: False},
        "app-bound-client.js": {app_bound: True, client: True},
        "key-dump-client.js": {output: True, client: True},
        "paths-only.sh": {
            "micro-behaviors/fs/path/application/browser::firefox-profiles-path": True,
            "micro-behaviors/fs/path/password-store::logins": True,
            "micro-behaviors/fs/path/cookie::cookies-binarycookies": True,
            "objectives/credential-access/browser/chromium::cookie-theft": False,
        },
        "schema-only.exe": {
            "micro-behaviors/data/serialize/schema-object::passwords-json-string-field": True,
            "micro-behaviors/data/serialize/schema-object::credit-cards-json-string-field": True,
            "micro-behaviors/data/serialize/schema-object::firefox-cookies-json-string-field": True,
            "objectives/credential-access/browser/multi-target::c2-browser-credential-harvest": False,
        },
        "abe-template.c": {
            "objectives/credential-access/browser/app-bound::abe-helper-dll-patch-template": True,
        },
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
            shutil.copyfile(root / "testdata/taxonomy/browser-access" / name, target)
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
