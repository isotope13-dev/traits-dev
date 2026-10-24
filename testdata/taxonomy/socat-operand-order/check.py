"""Check both socat address orders without executing any relay."""
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RELAY = "micro-behaviors/communications/proxy/relay::socat-tcp-shell-relay"
PTY = "objectives/command-and-control/reverse-shell/pty::socat"
CASES = {
    "tcp-first.sh": True,
    "exec-first.sh": True,
    "exec-first-ipv6.sh": True,
    "ordinary-relay.sh": False,
    "non-shell.sh": False,
    "separate-commands.sh": False,
}
result = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT), "--json",
     *[str(HERE / name) for name in CASES]],
    env=dict(os.environ, CLEAVE_SKIP_CACHE="1"),
    capture_output=True, text=True, check=True,
)
assert "warning" not in result.stderr.lower(), result.stderr
checked = set()
for line in result.stdout.splitlines():
    for report in json.loads(line).get("files", []):
        name = Path(report["path"]).name
        traits = {item["id"] for item in report.get("traits", [])}
        for trait in [RELAY, PTY]:
            assert (trait in traits) == CASES[name], (name, trait, traits)
        checked.add(name)
assert checked == CASES.keys(), checked
print(f"Passed {len(checked)} socat operand-order controls")
