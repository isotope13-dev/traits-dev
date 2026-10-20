#!/usr/bin/env python3
"""Check content-based CSV exclusions and their executable near misses."""
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

root = Path(__file__).resolve().parents[2]
cases = json.loads((Path(__file__).parent / "cases.json").read_text())["fixtures"]
with tempfile.TemporaryDirectory(prefix="fallout-cases-") as temporary:
    # Test-directory naming exclusions must not mask the positive controls.
    for case in cases:
        source = root / case["path"]
        shutil.copyfile(source, Path(temporary) / source.name)
    result = subprocess.run(
        ["cleave", "--traits-dir", str(root), "--format", "json", temporary],
        text=True, capture_output=True,
    )
    assert result.returncode == 0, result.stderr + result.stdout
    decoder = json.JSONDecoder()
    remaining = result.stdout.lstrip()
    reports = {}
    while remaining:
        report, end = decoder.raw_decode(remaining)
        for entry in report["files"]:
            reports[Path(entry["path"]).name] = {
                trait["id"] for trait in entry.get("traits", [])
            }
        remaining = remaining[end:].lstrip()
    for case in cases:
        name = Path(case["path"]).name
        actual = reports[name]
        missing = set(case["matched"]) - actual
        unexpected = set(case["not_matched"]) & actual
        assert not missing and not unexpected, (name, missing, unexpected)
        print("PASS", name)
