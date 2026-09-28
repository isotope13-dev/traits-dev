#!/usr/bin/env python3
"""Check source grouping and require separate source/transfer evidence roles.

Run separately from the verdict corpus: these assert individual findings, not
whole-file maliciousness. The example programs are scanned, never executed.
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
    stealer = "objectives/exfiltration/http/collect::python-profiled-http-collector"
    metrics = "micro-behaviors/communications/http/telemetry::python-tracking-metrics-json-upload"
    post = "micro-behaviors/communications/http/telemetry::python-aigc-post-marker"
    node = "objectives/exfiltration/stealer/credential::node-unix-secret-http-exfil"
    upload_target = "micro-behaviors/communications/ip/endpoint::js-external-http-upload-target"
    form_field = "micro-behaviors/communications/http/form::form-data-append"
    upload_call = "micro-behaviors/communications/http/upload::upload-file-js-method-call"
    ip_url = "micro-behaviors/communications/http/url/external-ip::url-external-ip-script"
    android = "objectives/exfiltration/stealer/credential::android-credential-upload-exfil"
    desktop = "micro-behaviors/hardware/display/screenshot::source-gdi-screen-capture-primitives"
    bitmap = "micro-behaviors/ui/graphics/image::source-gdi-compatible-bitmap"
    raster = "micro-behaviors/ui/graphics/draw::source-gdi-raster-copy"
    screen_export = "objectives/exfiltration/stealer/screen::browser-extension-screenshot-json-upload"
    tab_capture = "micro-behaviors/browser-extension/tabs::chrome-tabs-capture-visible"
    user_media = "micro-behaviors/hardware/input/media::browser-media-capture-api"
    recorder = "micro-behaviors/data/stream/record::media-stream-recorder"
    recording_export = "objectives/exfiltration/stealer/audiovisual::browser-av-recording-form-upload"
    cases = {
        "profile-and-secrets.py": {stealer: True},
        "profile-and-telemetry.py": {stealer: False, metrics: True, post: True},
        "node-endpoints-only.js": {node: False},
        "node-sources-only.js": {node: False},
        "node-source-collect.js": {node: True},
        "node-source-exfil.js": {node: True},
        "android-stores-post.kt": {android: True},
        "android-stores-header.kt": {android: True},
        "android-stores-local.kt": {android: False},
        "yarn-standalone.js": {"well-known/tool/packaging/yarn::yarn-standalone-bundle": True},
        "form-fields-and-ip.js": {upload_target: False, form_field: True, ip_url: True},
        "file-upload-to-ip.js": {upload_target: True, upload_call: True, ip_url: True},
        "offscreen-bitmap.cpp": {bitmap: True, raster: True, desktop: False},
        "desktop-bitmap.cpp": {bitmap: True, raster: True, desktop: True},
        "tab-capture-local.js": {tab_capture: True, screen_export: False},
        "tab-capture-upload.js": {
            tab_capture: True, screen_export: True,
            "micro-behaviors/communications/http/url/domain::js-remote-host-url": True,
        },
        "microphone-record-upload.js": {user_media: True, recorder: True, recording_export: True},
        "camera-record-upload.js": {user_media: True, recorder: True, recording_export: True},
        "synthetic-record-upload.js": {user_media: False, recorder: True, recording_export: False},
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
            shutil.copyfile(root / "testdata/taxonomy/stealer-source" / name, target)
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
