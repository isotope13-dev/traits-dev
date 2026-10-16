#!/usr/bin/env python3
"""Check popup record boundaries, geometry and language-independent payloads."""
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
AUTH = "objectives/credential-access/capture/network::notification-popup-webdav-authentication"
HIDE = "objectives/evasion/process/hidden/window::tiny-webdav-notification-popup"
EXPECTED = {
    "https-banner.ini": set(),
    "local-file.ini": set(),
    "localhost.ini": set(),
    "loopback.ini": set(),
    "local-and-remote.ini": {AUTH, HIDE},
    "visible-webdav.ini": {AUTH},
    "different-section.ini": {AUTH},
    "split-popups.ini": {AUTH},
    "commented-address.ini": set(),
    "non-popup.ini": set(),
    "width-ten.ini": {AUTH},
    "height-ten.ini": {AUTH},
    "case-whitespace-crlf.ini": {AUTH, HIDE},
    "renamed-endpoint.ini": {AUTH, HIDE},
    "writer.ps1": {AUTH, HIDE},
    "writer.cpp": {AUTH, HIDE},
    "prose.txt": set(),
}

result = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
     "--format", "jsonl", "analyze", *[str(HERE / name) for name in EXPECTED]],
    check=True, capture_output=True, text=True,
)
decoder = json.JSONDecoder()
remaining = result.stdout
seen = set()
while remaining.strip():
    report, end = decoder.raw_decode(remaining.lstrip())
    remaining = remaining.lstrip()[end:]
    for artifact in report.get("files", []):
        name = Path(artifact["path"]).name
        seen.add(name)
        observed = {
            trait["id"] for trait in artifact.get("traits", [])
            if trait["id"] in {AUTH, HIDE}
        }
        assert observed == EXPECTED[name], (name, observed, EXPECTED[name])
assert seen == set(EXPECTED), ("Missing fixtures", set(EXPECTED) - seen)
print(f"Passed {len(seen)} notification/WebDAV cases")
