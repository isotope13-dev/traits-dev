"""Check static capability rules without running the inspected Go code."""
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RULES = {
    "micro-behaviors/communications/tls/initialize::go-tls-client",
    "micro-behaviors/communications/tls/initialize::go-tls-listener",
    "micro-behaviors/communications/http/message::go-http2-new-framer",
    "micro-behaviors/fs/delete/file/syscall::go-syscall-unlink",
}
OLD = "micro-behaviors/communications/socket/ssl::go-tls-client"
command = [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
           "--format", "json", *map(str, sorted(HERE.glob("*.go")))]
result = subprocess.run(command, check=True, capture_output=True, text=True)
decoder = json.JSONDecoder()
remaining = result.stdout
files = {}
while remaining.strip():
    report, end = decoder.raw_decode(remaining.lstrip())
    remaining = remaining.lstrip()[end:]
    for file in report["files"]:
        files[Path(file["path"]).name] = {
            trait["id"]: trait for trait in file.get("traits", [])
        }
assert RULES <= files["operations.go"].keys()
assert not RULES.intersection(files["mentions.go"])
assert all(files["operations.go"][rule]["crit"] == 3 for rule in RULES)
assert all(OLD not in traits for traits in files.values())
description = files["subpackage.go"][
    "micro-behaviors/communications/grpc::grpc-go-import"]["desc"]
assert "subpackage" in description
print("PASS: TLS relocation, listener/framer/unlink calls, and non-call controls")
