"""Check relationships and near misses without executing sample code."""
import json
import pathlib
import subprocess

root = pathlib.Path(__file__).resolve().parents[3]
fixtures = pathlib.Path(__file__).resolve().parent
result = subprocess.run(
    ["cleave", "--traits-dir", str(root), "--format", "json", str(fixtures)],
    check=True, capture_output=True, text=True,
)
remaining = result.stdout.lstrip()
decoder = json.JSONDecoder()
reports = {}
while remaining:
    report, end = decoder.raw_decode(remaining)
    remaining = remaining[end:].lstrip()
    for item in report["files"]:
        reports[pathlib.Path(item["path"]).name] = item["traits"]

def ids(name):
    return {trait["id"] for trait in reports[name]}

relay = "micro-behaviors/communications/proxy/relay::native-socket-buffer-forwarding"
verify = "micro-behaviors/communications/tls/verify/disable::insecure-skip-verify"
dispatch = "objectives/command-and-control/remote-command/dispatch::"
assert relay in ids("socket-forward.c")
assert relay not in ids("socket-echo.c")
assert verify in ids("tls-config.go")
assert verify not in ids("tls-verified.go")
assert dispatch + "socket-buffer-shell-dispatch" in ids("socket-commands.c")
assert dispatch + "openssl-buffer-shell-dispatch" in ids("tls-commands.c")
assert sum(t["crit"] == 5 for t in reports["tls-commands.c"]) == 2
for control in ("tls-independent-command.c", "socket-echo.c", "tls-verified.go"):
    assert not [t for t in reports[control] if t["crit"] >= 4], control
print("PASS: receive/execute, forwarding, TLS configuration and near misses")
