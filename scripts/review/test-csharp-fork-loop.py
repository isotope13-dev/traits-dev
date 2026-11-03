#!/usr/bin/env python3
"""Detect an unconditional libc fork loop without flagging bounded workers."""

import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get("CLEAVE", str(ROOT.parent / "cleave/target/release/cleave"))
RULE = "objectives/impact/dos/fork-bomb::csharp-unbounded-libc-fork-loop"
SOURCE = '''\
using System.Runtime.InteropServices;
class Program {
    [DllImport("libc.so.6")] public static extern long fork();
    static void Main() { while (true) { fork(); } }
}
'''

with tempfile.TemporaryDirectory() as temp:
    for name, source, expected in (
        ("bomb", SOURCE, True),
        ("conditional", SOURCE.replace("fork(); }", "if (fork() == 0) { break; } }"), False),
        ("bounded", SOURCE.replace("while (true)", "while (running)"), False),
        ("wait", SOURCE.replace("fork(); }", "fork(); Wait(); }"), False),
        ("other_library", SOURCE.replace("libc.so.6", "libcustom.so.6"), False),
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

print("C# fork-loop boundaries passed")
