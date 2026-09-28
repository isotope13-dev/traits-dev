#!/usr/bin/env python3
"""Check mail source, access, send, and neutral record boundaries.

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
    address = "micro-behaviors/communications/email/address::email-domain-filter"
    smtp = "micro-behaviors/communications/email/send/direct::direct-smtp-c-source"
    worm = "objectives/lateral-movement/worm/email::direct-smtp-mass-mailer"
    select = "micro-behaviors/communications/email/access/imap::authenticated-imap-folder-selection"
    imap = "micro-behaviors/communications/email/access/imap::imap-cli-url"
    ews = "micro-behaviors/communications/email/access/exchange::exchange-web-services-client"
    collected = "objectives/collection/email-harvest::ews-mailbox-content-collection"
    sent = "micro-behaviors/communications/email/send/exchange::exchange-attachment-send"
    callback = "micro-behaviors/communications/tls/verify/callback::certificate-validation-callback-setter"
    identifier = "micro-behaviors/data/serialize/schema-object::api-id-guid-value"
    audit = "micro-behaviors/os/telemetry/logging/event::mailitems-access-application-api"
    recorded_client = "micro-behaviors/os/telemetry/logging/event::mail-access-rest-firefox-record"
    web_access = "micro-behaviors/communications/email/access/webmail::webmail-list-action-reference"
    web_collect = "objectives/collection/email-harvest::webmail-mailbox-harvest"
    web_export = "objectives/exfiltration/stealer/message::webmail-eml-exfiltration"
    cases = {
        "smtp-address-only.c": {address: True, smtp: True, worm: False},
        "smtp-mailstore.c": {address: True, smtp: True, worm: True},
        "imap-select.sh": {imap: True, select: True},
        "exchange-read.cs": {ews: True, collected: True, sent: False, callback: True},
        "exchange-send.cs": {ews: True, collected: False, sent: True},
        "api-fields.json": {identifier: True, audit: False},
        "mail-audit.json": {identifier: True, audit: True, recorded_client: True},
        "webmail-read.js": {web_access: True, web_collect: True, web_export: False},
        "webmail-export.js": {web_access: True, web_collect: True, web_export: True},
        "mapping-reads.py": {
            "micro-behaviors/data/collection/map::mapping-get-action-key": True,
            "micro-behaviors/data/collection/map::mapping-get-code-key": True,
            "micro-behaviors/data/collection/map::mapping-get-cookies-key": True,
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
            shutil.copyfile(root / "testdata/taxonomy/mail-source" / name, target)
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
