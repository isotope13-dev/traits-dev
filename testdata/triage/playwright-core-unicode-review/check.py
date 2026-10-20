#!/usr/bin/env python3
"""Character-code proximity must not turn Unicode/string helpers into evasion."""
import json
import os
from pathlib import Path
import shlex
import subprocess

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
fixtures = [HERE / "unicode-surrogates.html", HERE / "separate-functions.html"]
command = shlex.split(os.environ.get("CLEAVE", "cleave"))
result = subprocess.run(
    command + ["--traits-dir", str(ROOT), "--json"] + list(map(str, fixtures)),
    check=True, capture_output=True, text=True,
)
reports = [json.loads(line) for line in result.stdout.splitlines() if line.strip()]
files = [file for report in reports for file in report["files"]]
assert len(files) == len(fixtures), files
required = {
    "micro-behaviors/data/string/conversion::two-charcode-reads-in-expression",
    "micro-behaviors/data/string/conversion::fromcharcode-text-carrier",
}
for file in files:
    traits = {trait["id"]: trait for trait in file.get("traits", [])}
    assert required <= traits.keys(), (file["path"], traits)
    assert all(traits[id]["crit"] == 3 for id in required), traits
    elevated = [trait for trait in traits.values() if trait["crit"] >= 4]
    assert not elevated, (file["path"], elevated)
    print(Path(file["path"]).name + ": notable string operations; no suspicious/hostile findings")
