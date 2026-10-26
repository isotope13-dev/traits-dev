"""Focused regression test for the go-home-directory-wipe chain-home carve-out.

Runs cleave over the fixture sources in this directory and asserts the
expectations in cases.json: the Ignite-style `.Home()` accessor cleanup must
not match, while genuine user-home wipes still do.
"""
import json
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
ENV = dict(os.environ)
ENV.pop("CLEAVE_VALIDATE", None)

result = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
     "--format", "json", *map(str, sorted(HERE.glob("*.go")))],
    capture_output=True, text=True, check=True, env=ENV,
)
decoder = json.JSONDecoder()
remaining = result.stdout
files = {}
while remaining.strip():
    report, end = decoder.raw_decode(remaining.lstrip())
    remaining = remaining.lstrip()[end:]
    for entry in report["files"]:
        files[Path(entry["path"]).name] = {
            trait["id"] for trait in entry.get("traits", [])
        }

cases = json.loads((HERE / "cases.json").read_text())
failures = []
for name, expect in cases.items():
    if name not in files:
        failures.append(f"{name}: not analyzed")
        continue
    for trait in expect.get("matched", []):
        if trait not in files[name]:
            failures.append(f"{name}: expected match missing: {trait}")
    for trait in expect.get("not_matched", []):
        if trait in files[name]:
            failures.append(f"{name}: unexpected match: {trait}")

if failures:
    raise SystemExit("FAIL\n" + "\n".join(failures))
print(f"PASS: {len(cases)} cases")
