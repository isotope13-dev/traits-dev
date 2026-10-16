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
AUTH_SOURCE = AUTH + "-source"
HIDE_SOURCE = HIDE + "-source"
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
    "unc-ssl-popup.ini": {AUTH, HIDE},
    "unc-popup.ini": {AUTH, HIDE},
    "unc-localhost.ini": set(),
    "unc-loopback.ini": set(),
    "unc-smb-share.ini": set(),
    "unc-visible.ini": {AUTH},
    "unc-split-popup.ini": {AUTH},
    "unc-commented.ini": set(),
    "unc-mixed-separators.ini": set(),
    "writer.cs": {AUTH_SOURCE, HIDE_SOURCE},
    "writer.go": {AUTH_SOURCE, HIDE_SOURCE},
    "writer.rb": {AUTH_SOURCE, HIDE_SOURCE},
    "writer.js": {AUTH_SOURCE, HIDE_SOURCE},
}

result = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
     "--format", "jsonl", "analyze", *[str(HERE / name) for name in EXPECTED]],
    capture_output=True, text=True,
)
assert result.returncode == 0, result.stderr
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
            if trait["id"] in {AUTH, HIDE, AUTH_SOURCE, HIDE_SOURCE}
        }
        assert observed == EXPECTED[name], (name, observed, EXPECTED[name])
assert seen == set(EXPECTED), ("Missing fixtures", set(EXPECTED) - seen)
print(f"Passed {len(seen)} notification/WebDAV cases")
