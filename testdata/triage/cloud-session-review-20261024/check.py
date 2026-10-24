#!/usr/bin/env python3
"""Assert sensitive dual-use behavior without suppressing accurate findings."""
import json
import os
from pathlib import Path
import subprocess

here = Path(__file__).resolve().parent
root = here.parents[2]
run = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(root),
     "--format", "json", str(here / "integgri-conector-1.0.0.crx"),
     str(here / "session-with-decrypt.js"),
     str(here / "session-with-encrypt.js")],
    cwd=root, capture_output=True, text=True, check=True,
)
decoder = json.JSONDecoder()
remaining = run.stdout
reports = []
while remaining.strip():
    report, length = decoder.raw_decode(remaining.lstrip())
    remaining = remaining.lstrip()[length:]
    reports.extend(report["files"])

prefix = "objectives/credential-access/messaging/whatsapp::"
by_name = {Path(f["path"]).name: f for f in reports}
extension = by_name["integgri-conector-1.0.0.crx"]
assert not any(t["crit"] == 5 for f in reports for t in f.get("traits", []))
assert sum(t["crit"] == 4 for t in extension["traits"]) == 3
required = {
    prefix + "whatsapp-web-session-material-extraction",
    prefix + "whatsapp-session-extraction-with-json-post",
    "micro-behaviors/crypto/key/generate::webcrypto-generate-key-call",
    "micro-behaviors/crypto/key/export::webcrypto-export-key-call",
    "micro-behaviors/crypto/symmetric/aes/mode::javascript-aes-cbc-algorithm-literal",
}
assert required <= {t["id"] for t in extension["traits"]}
for name, expected in [("session-with-decrypt.js", True),
                       ("session-with-encrypt.js", False)]:
    observed = {t["id"] for t in by_name[name]["traits"]}
    assert ((prefix + "whatsapp-web-session-material-extraction") in observed) == expected
extractor = next(f for f in reports if f["path"].endswith("!!src/extractor.js"))
assert "micro-behaviors/process/inject/webextension::chrome-scripting-main-world" not in {
    t["id"] for t in extractor["traits"]
}
print("PASS: original connector, sensitive extraction, encryption-only near miss")
