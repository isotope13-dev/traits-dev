#!/usr/bin/env python3
"""Check popup record boundaries, geometry and language-independent payloads."""
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
AUTH = "micro-behaviors/ui/window/notify::notification-popup-webdav-address"
GEOMETRY = "micro-behaviors/ui/window/notify::tiny-webdav-notification-popup"
AUTH_SOURCE = AUTH + "-source"
GEOMETRY_SOURCE = GEOMETRY + "-source"
EXPECTED = {
    "https-banner.ini": set(),
    "local-file.ini": set(),
    "localhost.ini": set(),
    "loopback.ini": set(),
    "local-and-remote.ini": {AUTH, GEOMETRY},
    "visible-webdav.ini": {AUTH},
    "different-section.ini": {AUTH},
    "split-popups.ini": {AUTH},
    "commented-address.ini": set(),
    "non-popup.ini": set(),
    "width-ten.ini": {AUTH},
    "height-ten.ini": {AUTH},
    "case-whitespace-crlf.ini": {AUTH, GEOMETRY},
    "renamed-endpoint.ini": {AUTH, GEOMETRY},
    "writer.ps1": {AUTH, GEOMETRY},
    "writer.cpp": {AUTH, GEOMETRY},
    "prose.txt": set(),
    "unc-ssl-popup.ini": {AUTH, GEOMETRY},
    "unc-popup.ini": {AUTH, GEOMETRY},
    "unc-localhost.ini": set(),
    "unc-loopback.ini": set(),
    "unc-smb-share.ini": set(),
    "unc-visible.ini": {AUTH},
    "unc-split-popup.ini": {AUTH},
    "unc-commented.ini": set(),
    "unc-mixed-separators.ini": set(),
    "writer.cs": {AUTH_SOURCE, GEOMETRY_SOURCE},
    "writer.go": {AUTH_SOURCE, GEOMETRY_SOURCE},
    "writer.rb": {AUTH_SOURCE, GEOMETRY_SOURCE},
    "writer.js": {AUTH_SOURCE, GEOMETRY_SOURCE},
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
            if trait["id"] in {AUTH, GEOMETRY, AUTH_SOURCE, GEOMETRY_SOURCE}
        }
        assert observed == EXPECTED[name], (name, observed, EXPECTED[name])
        if name.startswith("writer."):
            high = [t for t in artifact.get("traits", []) if t["crit"] >= 4]
            assert not high, (name, high)
        for trait in artifact.get("traits", []):
            if trait["id"] in {AUTH, AUTH_SOURCE, GEOMETRY, GEOMETRY_SOURCE}:
                assert trait["crit"] == 3, (name, "configuration must be notable", trait)
            assert not trait["id"].startswith("objectives/evasion/process/hidden/window::tiny-webdav-notification-popup"), (name, trait)
            assert not trait["id"].startswith(
                "objectives/credential-access/capture/network::notification-popup-webdav-authentication"
            ), (name, "configuration is not authentication capture", trait)
assert seen == set(EXPECTED), ("Missing fixtures", set(EXPECTED) - seen)
print(f"Passed {len(seen)} notification/WebDAV cases")
