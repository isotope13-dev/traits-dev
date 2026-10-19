#!/usr/bin/env python3
"""Check the lifecycle acquisition and cookie-to-POST relationship separately."""
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
FIXTURES = Path(__file__).resolve().parent
READ = "objectives/credential-access/browser/extension::extension-install-unfiltered-cookie-read"
SEND = "objectives/exfiltration/stealer/browser::extension-cookie-callback-json-post"
EXPECTED = {
    "install-post.js": {READ, SEND},
    "renamed-direct.js": {READ, SEND},
    "unrelated-body.js": {READ},
    "wrong-jar.js": {READ},
    "non-body-shorthand.js": {READ},
    "overridden-body.js": {READ},
    "overridden-method.js": {READ},
    "reassigned-body.js": {READ},
    "scoped-cookie.js": set(),
    "user-export.js": {SEND},
    "quoted-source.js": set(),
    "comment-only.js": set(),
    "unrelated-callback.js": {READ},
}
result = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
     "--format", "json", *[str(FIXTURES / name) for name in EXPECTED]],
    check=True, text=True, stdout=subprocess.PIPE,
)
# Multi-input JSON output can contain successive objects without separators.
decoder = json.JSONDecoder()
remaining = result.stdout
seen = {}
while remaining.strip():
    remaining = remaining.lstrip()
    report, end = decoder.raw_decode(remaining)
    remaining = remaining[end:]
    for file in report["files"]:
        name = Path(file["path"]).name
        actual = {trait["id"] for trait in file.get("traits", [])} & {READ, SEND}
        if name in EXPECTED:
            seen[name] = seen.get(name, set()) | actual
assert set(seen) == set(EXPECTED), (set(seen), set(EXPECTED))
for name, expected in EXPECTED.items():
    assert seen[name] == expected, (name, seen[name], expected)
print(f"PASS: {len(EXPECTED)} cookie callback and lifecycle controls")
