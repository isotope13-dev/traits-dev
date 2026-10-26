#!/usr/bin/env python3
"""Check capability corrections and retain independent attack fixtures."""
import hashlib
import json
import os
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PREFIX = "micro-behaviors/"
HOST = PREFIX + "os/sysinfo/hostname::node-hostname-buffer"
COMPILE = PREFIX + "os/module/load::module-compile-marker"
WEBCLIENT = PREFIX + "communications/http/client/managed::webclient-data-type"
COPY = PREFIX + "fs/file/copy::cp-command-text"
ROLE = PREFIX + "os/security/auth/rbac::check-permission-or-role-call"
EVENT = PREFIX + "ui/window/form-input::browser-json-event-value-send-call"
ED = PREFIX + "crypto/sign::ed25519-sign-call"
EC = PREFIX + "crypto/sign::secp256k1-sign-call"
DEFLATE = PREFIX + "data/compress/zlib::javascript-deflate-call"
NX = PREFIX + "fs/write/content::nx-devkit-generate-files"
CASES = {
    "hostname-slice.js": ({HOST}, set()),
    "array-slice.js": (set(), {HOST}),
    "compile-module.js": ({COMPILE}, set()),
    "compile-transaction.js": (set(), {COMPILE}),
    "webclient-data.bin": ({WEBCLIENT}, set()),
    "slack-map.json": (set(), {WEBCLIENT}),
    "copy-command.js": ({COPY}, set()),
    "codepoint.js": (set(), {COPY}),
    "permission.js": ({ROLE}, set()),
    "permission-label.ts": (set(), {ROLE}),
    "json-event.html": ({EVENT}, set()),
    "unrelated-event.html": (set(), {EVENT}),
    "noble-sign.ts": ({ED, EC}, set()),
    "not-sign.ts": (set(), {ED, EC}),
    "deflate.ts": ({DEFLATE}, set()),
    "not-deflate.ts": (set(), {DEFLATE}),
    "nx-generate.js": ({NX}, set()),
    "not-nx-generate.js": (set(), {NX}),
}


def documents(text):
    decoder = json.JSONDecoder()
    while text.strip():
        doc, end = decoder.raw_decode(text.lstrip())
        yield doc
        text = text.lstrip()[end:]


def main():
    retained = json.loads((HERE / "retained-controls.json").read_text())
    paths = [HERE / name for name in CASES]
    paths.extend(ROOT / row["path"] for row in retained)
    for row in retained:
        digest = hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest()
        assert digest == row["sha256"], row["path"]
    result = subprocess.run(
        [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
         "--format", "json", *map(str, paths)],
        capture_output=True, text=True, check=True,
    )
    assert "warn" not in result.stderr.lower(), result.stderr
    reports = {
        str(Path(doc["files"][0]["path"]).resolve()): doc["files"][0]
        for doc in documents(result.stdout)
    }
    for name, (present, absent) in CASES.items():
        traits = {t["id"] for t in reports[str(HERE / name)].get("traits", [])}
        assert present <= traits, (name, "missing", present - traits)
        assert not absent & traits, (name, "unexpected", absent & traits)
    for row in retained:
        traits = {t["id"]: t["crit"] for t in
                  reports[str(ROOT / row["path"])].get("traits", [])}
        for trait, severity in row["retain"].items():
            assert traits.get(trait, 0) >= severity, (row["path"], trait)
    print(f"Passed {len(CASES)} capability cases and {len(retained)} existing controls")


if __name__ == "__main__":
    main()
