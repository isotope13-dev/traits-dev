#!/usr/bin/env python3
"""Bind a Discord command parameter to local keystroke injection."""

import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get("CLEAVE", str(ROOT.parent / "cleave/target/release/cleave"))
RULE = "objectives/command-and-control/backdoor/control/discord::csharp-discord-command-sends-keys"
SOURCE = '''\
class Handler : ModuleBase<SocketCommandContext> {
    [Command("type")]
    void Type(string input) { SendKeys.SendWait(input); }
}
'''

with tempfile.TemporaryDirectory() as temp:
    for name, source, expected in (
        ("command", SOURCE, True),
        ("different_input", SOURCE.replace("SendWait(input)", "SendWait(other)"), False),
        ("constant", SOURCE.replace("SendWait(input)", 'SendWait("hello")'), False),
        ("different_context", SOURCE.replace("SocketCommandContext", "LocalContext"), False),
        ("no_command", SOURCE.replace('[Command("type")]', ""), False),
    ):
        path = Path(temp) / f"{name}.cs"
        path.write_text(source)
        result = subprocess.run(
            [CLEAVE, "--traits-dir", str(ROOT), "--all-files", "--format=json", str(path)],
            check=True, capture_output=True, text=True,
            env={**os.environ, "CLEAVE_SKIP_CACHE": "1"},
        )
        report = json.loads(result.stdout)
        found = any(t["id"] == RULE for f in report["files"] for t in f.get("traits", []))
        assert found == expected, (name, found)

print("C# Discord keystroke command boundaries passed")
