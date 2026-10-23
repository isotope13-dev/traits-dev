"""Scan static fixtures only; never execute the Go sources."""
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
ENV = dict(os.environ)
ENV.pop("CLEAVE_VALIDATE", None)
result = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
     "--format", "json", *map(str, sorted(HERE.glob("*.go")))],
    capture_output=True, text=True, check=True, env=ENV,
)
decoder = json.JSONDecoder()
remaining = result.stdout
files = {}
while remaining.strip():
    report, end = decoder.raw_decode(remaining.lstrip())
    remaining = remaining.lstrip()[end:]
    for file in report["files"]:
        files[Path(file["path"]).name] = {
            trait["id"]: trait["crit"] for trait in file.get("traits", [])
        }
dial = "micro-behaviors/communications/grpc::grpc-go-dial"
client = "micro-behaviors/communications/grpc::grpc-go-client"
listen = "micro-behaviors/communications/socket/listen::listen-go"
accept = "micro-behaviors/communications/socket/accept::accept-go"
bind = "objectives/command-and-control/backdoor/bind-shell::go-bind-shell-stdio-source"
for name in ["context-client.go", "legacy-client.go"]:
    assert files[name][dial] == files[name][client] == 3
local = "micro-behaviors/communications/grpc::grpc-go-local-client"
assert files["local-client.go"][local] == 3
assert local not in files["other-local-dial.go"]
assert files["listener_test.go"][listen] == 3
assert dial not in files["references.go"]
assert listen not in files["references.go"]
assert accept not in files["references.go"]
for name in ["bind-shell.go", "bind-shell_test.go"]:
    assert files[name][listen] == files[name][accept] == 3
    assert files[name][bind] == 5
for name in ["context-client.go", "legacy-client.go", "listener_test.go", "references.go"]:
    assert not [trait for trait, crit in files[name].items() if crit >= 4], name
print("PASS: parsed RPC calls, listener tests, references, and renamed bind shell")
