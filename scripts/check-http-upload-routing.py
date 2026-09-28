#!/usr/bin/env python3
"""Check HTTP source, transfer, and neutral capability boundaries.

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
    B = "micro-behaviors/"
    E = "objectives/exfiltration/"
    hybrid = B + "crypto/hybrid::openssl-rsa-aes-hybrid-encryption"
    hybrid_export = E + "http/encrypted::hybrid-encrypt-exfil"
    envelope = B + "crypto/hybrid::webcrypto-hybrid-payload-envelope"
    envelope_export = E + "http/encrypted::browser-webcrypto-hybrid-http-exfil"
    tar = B + "data/archive/create/tar::shell-tar-create-file"
    archive_export = E + "http/archive::shell-staged-tar-http-upload"
    form = B + "communications/http/form::image-formdata-with-user-id"
    image_export = E + "stealer/image::all-site-extension-image-upload"
    profiler = E + "stealer/multi-source::python-profiler"
    browser_source = "objectives/credential-access/browser/multi-target::system-info-with-browser"
    wallet_source = "objectives/credential-access/wallet/crypto::system-info-with-wallet"
    curl_sink = B + "communications/http/upload::curl-file-upload-exfil"
    cases = {
        "profiler-upload.py": {browser_source: True, wallet_source: True, curl_sink: True, profiler: True},
        "profiler-local.py": {browser_source: True, wallet_source: True, curl_sink: False, profiler: False},
        "profiler-no-wallet.py": {browser_source: True, wallet_source: False, curl_sink: True, profiler: False},
        "image-header.m": {
            B + "communications/http/header/content-type::image-ppm-content-type": True,
            B + "communications/http/request/body::objc-curlopt-postfields": True,
            E + "http/upload::objc-libcurl-agent-upload": False,
        },
        "chunk-header.js": {
            B + "communications/http/header/transfer-encoding::node-chunked-transfer-encoding": True,
            E + "stealer/appliance-config::openwrt-node-chunked-http-exfil": False,
        },
        "form-local.js": {form: True, image_export: False},
        "archive-local.sh": {tar: True, archive_export: False},
        "archive-upload.sh": {tar: True, archive_export: True},
        "archive-local.ps1": {
            B + "data/archive/create/zip::powershell-compress-archive": True,
            B + "data/archive/create/utility::windows-archive-create": True,
            E + "http/archive::windows-encoded-archive-http-exfil": False,
        },
        "hybrid-local.sh": {hybrid: True, hybrid_export: False},
        "hybrid-upload.sh": {hybrid: True, hybrid_export: True},
        "envelope-local.js": {envelope: True, envelope_export: False},
        "envelope-upload.js": {envelope: True, envelope_export: True},
        "torrent-local.sh": {
            B + "data/serialize/bittorrent::bittorrent-cli-web-seeded-archive-release": True,
            B + "data/serialize/bittorrent::bittorrent-cli-archive-staging": True,
        },
        "config-path.c": {
            B + "fs/path/os/identity::openwrt-release-or-banner-path": True,
            B + "os/sysinfo/network::openwrt-uci-recon-command": True,
            B + "communications/http/url/api-path::native-http-message-api-path": True,
            E + "stealer/system-info/network::openwrt-uci-host-profile-http-exfil": False,
        },
        "upload-prompt.sh": {B + "ui/dialog/prompt::encrypted-metadata-upload-prompt": True},
        "groovy-post.groovy": {
            B + "communications/http/request/body::groovy-http-post-output": True,
            B + "communications/http/url/endpoint::groovy-upload-url-construction": True,
            E + "stealer/file::groovy-http-file-upload": False,
        },
        "schema-local.py": {B + "data/serialize/schema-object::credential-var-in-dict": True},
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
            shutil.copyfile(root / "testdata/taxonomy/http-upload" / name, target)
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
