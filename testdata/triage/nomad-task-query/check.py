#!/usr/bin/env python3
"""Check prompt-query near misses and corrected neutral trait placements."""
import json
from pathlib import Path
import subprocess

here = Path(__file__).resolve().parent
root = here.parents[2]
result = subprocess.run(
    ["cleave", "--traits-dir", str(root), "--format", "json", "analyze", str(here)],
    capture_output=True, text=True, check=False,
)
assert result.returncode == 0, result.stderr or result.stdout
s = result.stdout
decoder = json.JSONDecoder()
observed = {}
while s.strip():
    s = s.lstrip()
    report, end = decoder.raw_decode(s)
    s = s[end:]
    for file in report.get("files", []):
        observed[Path(file["path"]).name] = {t["id"] for t in file.get("traits", [])}
checks = 0
failures = []
for name, expected in json.loads((here / "cases.json").read_text()).items():
    assert name in observed, f"Missing fixture: {name}"
    for trait, wanted in expected.items():
        checks += 1
        if (trait in observed[name]) != wanted:
            failures.append(f"{name}: {trait} expected {wanted}")
assert not failures, "\n".join(failures)
print(f"{checks} trait assertions passed")
