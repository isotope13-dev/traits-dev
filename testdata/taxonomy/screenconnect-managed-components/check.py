#!/usr/bin/env python3
"""Check compiled CLR name boundaries without running fixture assemblies."""
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
EXPECTED = {
    "micro-behaviors/data/property/assign::dotnet-item-setter-token",
    "micro-behaviors/fs/path/basename::service-suffix-executable-reference",
    "micro-behaviors/ui/controls/widget::windows-file-open-dialog-interface",
}
RETIRED = "micro-behaviors/os/service/identity::service-executable-filename"
engine = sys.argv[1] if len(sys.argv) > 1 else "cleave"
for name, expected in [("IndexerPicker.dll", EXPECTED), ("ItemsEnabled.dll", set())]:
    result = subprocess.run(
        [engine, "--traits-dir", str(ROOT), "--format", "json", str(HERE / name)],
        check=True, capture_output=True, text=True,
    )
    report = json.loads(result.stdout)
    ids = {trait["id"] for item in report["files"] for trait in item.get("traits", [])}
    assert ids & EXPECTED == expected, (name, ids & EXPECTED, expected)
    assert RETIRED not in ids, (name, RETIRED)
    print(f"PASS {name}: {len(expected)} expected observations")
