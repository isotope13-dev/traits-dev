#!/usr/bin/env python3
"""Check generated AMSI-bypass output and inert near misses."""

import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get("CLEAVE", str(ROOT.parent / "cleave/target/release/cleave"))
RULE = "objectives/evasion/anti-av/amsi::csharp-prints-transformed-amsi-bypass"
SOURCE = '''\
using System;
class Program {
    static string Generate() {
        var payload = "[Ref].Assembly.GetType('AmsiUtils').GetField('amsiInitFailed','NonPublic,Static').SetValue($null,$true)";
        switch (1) { case 1: return Transform(payload); default: return ""; }
    }
    static string Transform(string s) { return s; }
    static void Main() { Console.WriteLine(Generate()); }
}
'''

with tempfile.TemporaryDirectory() as temp:
    for name, source, expected in (
        ("generator", SOURCE, True),
        ("different_payload", SOURCE.replace("Transform(payload)", "Transform(other)"), False),
        ("not_printed", SOURCE.replace("Console.WriteLine(Generate())", "Console.WriteLine(other())"), False),
        ("false_value", SOURCE.replace("$true", "$false"), False),
        ("no_field_lookup", SOURCE.replace("GetField", "ReadField"), False),
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

print("C# AMSI generator boundaries passed")
