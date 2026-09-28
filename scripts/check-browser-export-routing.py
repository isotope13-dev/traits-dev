#!/usr/bin/env python3
"""Check browser export, local acquisition, and cookie capability boundaries.

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
    export = "objectives/exfiltration/stealer/browser::facebook-session-cookie-tls-export"
    fields = "objectives/credential-access/browser/safari::objectivec-facebook-session-cookie-fields"
    tls = "micro-behaviors/communications/socket/ssl::objectivec-ssl-write-reference"
    module = "micro-behaviors/communications/http/cookies::browser-cookie3-module-reference"
    jar = "micro-behaviors/communications/http/cookie-store::aiohttp-cookiejar-module-marker"
    archive = "micro-behaviors/data/archive/custom::pyinstaller-archive-cookie-read-error"
    extension = "objectives/exfiltration/stealer/browser::chromium-extension-storage-http-exfil"
    acquisition = "objectives/credential-access/browser/chromium::chromium-extension-storage-collection"
    headless = "objectives/exfiltration/stealer/browser::silent-headless-browser-credential-exfil"
    profile = "objectives/credential-access/browser/chromium::silent-headless-browser-profile"
    cases = {
        "headless-export.py": {profile: True, headless: True},
        "headless-local.py": {profile: True, headless: False},
        "cookie-export.m": {fields: True, tls: True, export: True},
        "cookie-local.m": {fields: True, tls: False, export: False},
        "tls-only.m": {fields: False, tls: True, export: False},
        "browser-module.py": {module: True, jar: False, archive: False},
        "cookiejar-module.py": {module: False, jar: True, archive: False},
        "archive-cookie.py": {module: False, jar: False, archive: True},
        "extension-export.js": {acquisition: True, extension: True},
        "extension-local.js": {acquisition: True, extension: False},
        "store-and-wallet.c": {
            "micro-behaviors/fs/path/application/browser::chromium-browser-store-set": True,
            "micro-behaviors/crypto/library/blockchain/brand-wallet::wallet-brand-metamask": True,
        },
        "adhoc-notes-client.macho": {
            "metadata/signed/trust-level::adhoc": True,
            "micro-behaviors/communications/http/download/curl::macos-libcurl-http": True,
            "micro-behaviors/fs/path/personal::apple-notes-store": True,
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
            shutil.copyfile(root / "testdata/taxonomy/browser-export-final" / name, target)
            result = subprocess.run(
                [args.cleave, "--traits-dir", str(root), "test-rules", "--rules",
                 ",".join(expected), str(target)],
                capture_output=True, text=True, check=True,
            )
            if name in {"store-and-wallet.c", "adhoc-notes-client.macho"}:
                scan = subprocess.run(
                    [args.cleave, "--traits-dir", str(root), "--format", "json", str(target)],
                    capture_output=True, text=True, check=True,
                )
                emitted = {trait["id"] for file in json.loads(scan.stdout)["files"]
                           for trait in file.get("traits", [])}
                assert not any(rule.startswith("objectives/exfiltration/stealer/browser::")
                               for rule in emitted), (name, emitted)
                print(f"PASS {name}: no browser-export verdict", flush=True)
        output = result.stdout + result.stderr
        for rule, matched in expected.items():
            marker = ("MATCHED " if matched else "NOT MATCHED ") + rule + " "
            if not any(line.startswith(marker) for line in output.splitlines()):
                raise AssertionError(f"{name}: expected {marker.strip()}\n{output}")
        print(f"PASS {name}: {len(expected)} finding assertions", flush=True)


if __name__ == "__main__":
    main()
