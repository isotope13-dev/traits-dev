#!/usr/bin/env python3
"""Check source binding and taxonomy placement with positive/near-miss pairs."""
import json
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[2]
fixture_root = Path(__file__).resolve().parent
checks = 0
failures = []
for suite in ("clipboard-source-link", "trait-placement"):
    directory = fixture_root / suite
    cases = json.loads((directory / "cases.json").read_text())
    result = subprocess.run(
        ["cleave", "--traits-dir", str(root), "--all-files", "--format", "json", str(directory)],
        text=True, capture_output=True, check=False,
    )
    if result.returncode:
        raise RuntimeError(result.stderr or result.stdout)
    decoder = json.JSONDecoder()
    remaining = result.stdout
    observed = {}
    while remaining.strip():
        report, end = decoder.raw_decode(remaining.lstrip())
        remaining = remaining.lstrip()[end:]
        for file in report["files"]:
            observed[Path(file["path"]).name] = {trait["id"] for trait in file.get("traits", [])}
    for name, expectations in cases.items():
        if name not in observed:
            failures.append(f"Fixture was not analyzed: {name}")
            continue
        for trait, expected in expectations.items():
            if (trait in observed[name]) != expected:
                failures.append(f"{name}: {trait} expected {expected}")
            checks += 1
assert not failures, "\n".join(failures)
print(f"{checks} trait assertions passed")
