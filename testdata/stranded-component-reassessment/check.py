#!/usr/bin/env python3
"""Verify relocated observations against native code and nearby reference forms."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

here = Path(__file__).resolve().parent
root = here.parent.parent
fixtures = root / "testdata" / "benign" / "stranded-component-reassessment"
header = "micro-behaviors/communications/http/header/set::go-http-header-set-string"
packages = {
    "metadata/import/builtin::go-net-http-symbol-reference",
    "metadata/import/builtin::go-crypto-aes-symbol-reference",
    "metadata/import/builtin::go-crypto-cipher-symbol-reference",
    "metadata/import/builtin::go-crypto-tls-symbol-reference",
}


def traits(path):
    report = json.loads(subprocess.check_output([
        os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(root),
        "--format", "json", str(path),
    ], text=True))
    return {t["id"] for f in report["files"] for t in f.get("traits", [])}


assert header in traits(fixtures / "header-set.py")
assert header not in traits(fixtures / "header-get.py")
assert header not in traits(fixtures / "generic-set.py")
assert not packages & traits(fixtures / "package-names.py")
with tempfile.TemporaryDirectory() as tmp:
    binary = Path(tmp) / "stdlib-control.elf"
    env = dict(os.environ, CGO_ENABLED="0", GOOS="linux", GOARCH="amd64")
    subprocess.run(["go", "build", "-o", str(binary), str(fixtures / "stdlib-control.go")],
                   env=env, check=True)
    actual = traits(binary)
    assert packages <= actual, packages - actual
    assert "metadata/lang/compiler/systems::go-binary" in actual
print("Five relocated observations and independent compiler context verified.")
