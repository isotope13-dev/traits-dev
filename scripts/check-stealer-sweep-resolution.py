#!/usr/bin/env python3
"""Protect the credential-source plus transfer boundary for native stealer rules."""

import argparse
from pathlib import Path
import subprocess
import tempfile


def main():
    root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cleave", default=str(root.parent / "cleave/target/release/cleave"))
    args = parser.parse_args()

    transfer_first = "micro-behaviors/communications/transfer::native-upload-before-snapshot-language"
    transfer_last = "micro-behaviors/communications/transfer::native-snapshot-before-upload-language"
    transfer_phrase = "micro-behaviors/communications/transfer::native-snapshot-upload-language"
    credential_source = "micro-behaviors/os/security/auth/secret::native-credential-snapshot-language"
    token_source = "micro-behaviors/os/security/auth/secret::native-token-capture-language"
    root_rule = "objectives/exfiltration/stealer/credential::native-credential-snapshot-tunnel"
    rules = ",".join((transfer_first, transfer_last, transfer_phrase, credential_source,
                       token_source, root_rule))
    cases = {
        "credential-snapshot-then-upload": (
            "credential snapshot export upload https://agent.trycloudflare.com",
            {transfer_last: True, transfer_phrase: True, credential_source: True,
             token_source: False, root_rule: True},
        ),
        "token-upload-then-capture": (
            "upload snapshot token capture https://agent.trycloudflare.com",
            {transfer_first: True, transfer_phrase: True, credential_source: False,
             token_source: True, root_rule: True},
        ),
        "source-and-tunnel-without-transfer": (
            "credential snapshot export https://agent.trycloudflare.com",
            {transfer_first: False, transfer_last: False, transfer_phrase: False,
             credential_source: True, token_source: False, root_rule: False},
        ),
        "transfer-and-tunnel-without-sensitive-source": (
            "generic snapshot export upload https://agent.trycloudflare.com",
            {transfer_last: True, transfer_phrase: True, credential_source: False,
             token_source: False, root_rule: False},
        ),
        "source-and-transfer-without-tunnel": (
            "credential snapshot export upload without a tunnel",
            {transfer_last: True, transfer_phrase: True, credential_source: True,
             token_source: False, root_rule: False},
        ),
    }

    with tempfile.TemporaryDirectory(prefix="stealer-sweep-") as temp:
        for name, (body, expected) in cases.items():
            target = Path(temp) / f"{name}.elf"
            target.write_bytes(b"\x7fELF\x02\x01\x01" + b"\0" * 9 + body.encode())
            result = subprocess.run(
                [args.cleave, "--traits-dir", str(root), "test-rules", "--rules", rules, str(target)],
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
