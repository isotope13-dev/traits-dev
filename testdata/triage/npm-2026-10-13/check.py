#!/usr/bin/env python3
"""Static controls for Rust TLS paths and neutral browser-store observations.

Compile inert string carriers; analyze them without executing the binaries.
Run from the repository root with python3 testdata/triage/npm-2026-10-13/check.py.
"""
import json
import pathlib
import subprocess
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[3]
RUSTLS = "micro-behaviors/crypto/library/provider::rustls-crate-path"
GO_TLS = "micro-behaviors/data/runtime/library::go-tls-ciphersuites-reference"
KEY = "micro-behaviors/data/config/browser-preference::chromium-key-storage-reference"
COOKIE = "micro-behaviors/fs/path/cookie::cookie-sqlite-database-reference"
OLD_KEY = "well-known/lib/platform/browser-automation/drivers/selenium::browser-profile-chrome-key-material"
OLD_COOKIE = "objectives/supply-chain/hidden-payload/extensions/backdoor::extension-cookie-database-reference"


def findings(path):
    result = subprocess.run(
        ["cleave", "--traits-dir", str(ROOT), "--format", "json", str(path)],
        check=True, capture_output=True, text=True,
    )
    return {t["id"] for t in json.loads(result.stdout)["files"][0]["traits"]}


with tempfile.TemporaryDirectory(prefix="npm-triage-controls-") as directory:
    base = pathlib.Path(directory)
    cases = [
        ("windows-rustls", r"C:\build\rustls-0.23.32\src\msgs\handshake.rs", True),
        ("unix-rustls", "/build/rustls-0.23.32/src/msgs/handshake.rs", True),
        ("mixed-rustls", r"/build/rustls-0.23.32\src/msgs/handshake.rs", True),
        ("different-crate", r"C:\build\not-rustls-0.23.32\src\tls.rs", False),
        ("different-directory", r"C:\build\rustls-0.23.32\tests\tls.rs", False),
        ("go-tls-control", "/build/crypto/tls/handshake.go", False),
    ]
    for name, build_path, expected in cases:
        source = base / (name + ".c")
        binary = base / (name + ".bin")
        source.write_text(
            "#include <stdio.h>\nint main(void) { puts(" + json.dumps(build_path)
            + '); puts("CipherSuites"); return 0; }\n'
        )
        subprocess.run(["cc", "-O0", str(source), "-o", str(binary)], check=True)
        ids = findings(binary)
        assert (RUSTLS in ids) == expected, (name, ids)
        # A bare CipherSuites token is shared by unrelated TLS libraries.
        assert GO_TLS not in ids, (name, ids)
        print(name + ": PASS")

    for name, token, expected in [
        ("qualified-go-tls", "crypto/tls.CipherSuites", True),
        ("qualified-go-tls-slash", "crypto/tls/CipherSuites", True),
        ("objc-socket-tls-option", "GCDAsyncSocketSSLCipherSuites", False),
        ("different-go-function", "crypto/tls.CipherSuitesExtra", False),
    ]:
        source = base / (name + ".c")
        binary = base / (name + ".bin")
        source.write_text(
            "#include <stdio.h>\nint main(void) { puts(" + json.dumps(token)
            + "); return 0; }\n"
        )
        subprocess.run(["cc", "-O0", str(source), "-o", str(binary)], check=True)
        ids = findings(binary)
        assert (GO_TLS in ids) == expected, (name, ids)
        print(name + ": PASS")

    for name, contents, expected in [
        ("cookie-reader", 'const service = "Chrome Safe Storage"; const db = "cookies.sqlite";', {KEY, COOKIE}),
        ("key-field", 'const field = "os_crypt";', {KEY}),
        ("singular-cookie", 'const db = "COOKIE.SQLITE";', {COOKIE}),
        ("unrelated", 'const db = "application.sqlite"; const service = "other";', set()),
    ]:
        source = base / (name + ".js")
        source.write_text(contents + "\n")
        ids = findings(source)
        assert ids.intersection({KEY, COOKIE}) == expected, (name, ids)
        assert not ids.intersection({OLD_KEY, OLD_COOKIE}), (name, ids)
        print(name + ": PASS")
