"""Scan controls without compiling or executing the inspected Go code."""
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
EXPECTED = {
    "micro-behaviors/communications/grpc::grpc-go-server-keepalive",
    "micro-behaviors/communications/grpc::grpc-go-client-keepalive",
    "micro-behaviors/communications/grpc::grpc-go-keepalive-enforcement",
    "micro-behaviors/communications/tls/initialize::grpc-go-client-tls-from-file",
    "micro-behaviors/communications/tls/initialize::grpc-go-server-tls-from-file",
}

result = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
     "--format", "jsonl", str(HERE / "operations.go"), str(HERE / "mentions.go")],
    check=True, capture_output=True, text=True,
)
assert not result.stderr.strip(), result.stderr
files = {
    Path(file["path"]).name: {t["id"]: t["crit"] for t in file.get("traits", [])}
    for line in result.stdout.splitlines()
    for file in json.loads(line)["files"]
}
assert EXPECTED <= files["operations.go"].keys()
assert all(files["operations.go"][rule] == 3 for rule in EXPECTED)
assert not EXPECTED & files["mentions.go"].keys()
print("PASS: five notable API calls; no comment, string or other-receiver matches")
