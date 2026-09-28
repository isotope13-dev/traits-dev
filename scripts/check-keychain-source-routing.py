#!/usr/bin/env python3
"""Check secret-store sources and local acquisition versus remote export.

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
    gaming = "objectives/credential-access/gaming/mobile::lua-gamecenter-keychain-targeting"
    game_export = "objectives/exfiltration/stealer/keychain::ios-keychain-credential-exfil"
    field = "micro-behaviors/os/security/keychain::swift-keychain-output-field"
    swift_export = "objectives/exfiltration/stealer/keychain::swift-ios-keychain-http-exfil"
    local_stores = "objectives/credential-access/theft/multi-store::ruby-keychain-ssh-harvest"
    ruby_export = "objectives/exfiltration/stealer/credential::ruby-credential-http-export"
    shell_extract = "objectives/credential-access/keychain/extract::shell-keychain-dump-with-secret-queries"
    shell_export = "objectives/exfiltration/stealer/credential::shell-secret-http-export"
    dpapi_export = "objectives/exfiltration/stealer/credential::dpapi-secret-webhook-export"
    dpapi = "micro-behaviors/os/security/dpapi::python-dpapi-unprotect"
    cases = {
        "gamecenter-local.lua": {gaming: True, game_export: False},
        "gamecenter-network.lua": {gaming: True, game_export: True},
        "keychain-local.swift": {field: True, swift_export: False},
        "keychain-post.swift": {field: True, swift_export: True},
        "keychain-ssh-local.rb": {local_stores: True, ruby_export: False},
        "keychain-post.rb": {local_stores: False, ruby_export: True},
        "discord-post.rb": {ruby_export: True},
        "keychain-local.sh": {shell_extract: True, shell_export: False},
        "keychain-upload.sh": {shell_extract: True, shell_export: True},
        "dpapi-webhook.py": {dpapi: True, dpapi_export: True},
        "dpapi-local.py": {dpapi: True, dpapi_export: False},
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
            shutil.copyfile(root / "testdata/taxonomy/keychain-source" / name, target)
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
