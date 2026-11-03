#!/usr/bin/env python3
"""Check the AMSI name and memory-operation co-occurrence boundary."""

import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get("CLEAVE", str(ROOT.parent / "cleave/target/release/cleave"))
RULE = "metadata/file/profile/memory/protection-context::powershell-amsi-protect-copy-cooccurrence"
SOURCE = '''\
$target = "AmsiScanBuffer"
$protect = "VirtualProtect"
[System.Runtime.InteropServices.Marshal]::Copy($bytes, 0, $pointer, 6)
'''

with tempfile.TemporaryDirectory() as temp:
    for name, source, expected in (
        ("cooccurrence", SOURCE, True),
        ("no_amsi", SOURCE.replace("AmsiScanBuffer", "AnotherExport"), False),
        ("no_protect", SOURCE.replace("VirtualProtect", "OtherProtect"), False),
        ("no_copy", SOURCE.replace("::Copy", "::ReadByte"), False),
    ):
        path = Path(temp) / f"{name}.ps1"
        path.write_text(source)
        result = subprocess.run(
            [CLEAVE, "--traits-dir", str(ROOT), "--all-files", "--format=json", str(path)],
            check=True, capture_output=True, text=True,
            env={**os.environ, "CLEAVE_SKIP_CACHE": "1"},
        )
        report = json.loads(result.stdout)
        found = any(t["id"] == RULE for f in report["files"] for t in f.get("traits", []))
        assert found == expected, (name, found)

print("PowerShell AMSI/protect/copy boundaries passed")
