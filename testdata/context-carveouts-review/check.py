"""Focused regression tests for benign-context carve-outs.

Scan-output assertions (matched/not_matched) cover atomic traits, which the
scan always emits. Composite assertions (rules_matched/rules_not_matched)
run through `cleave test-rules`, because the scan filters low-value `any:`
composites from its output while still evaluating them internally.
"""
import json
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
ENV = dict(os.environ)
ENV.pop("CLEAVE_VALIDATE", None)

targets = sorted(HERE.glob("*.sh")) + sorted(HERE.glob("*.py")) + sorted(HERE.glob("*.c"))
result = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
     "--format", "json", *map(str, targets)],
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
rule_checks = {}
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
    for key, flag in (("rules_matched", True), ("rules_not_matched", False)):
        for rule in expect.get(key, []):
            rule_checks.setdefault(rule, []).append((name, flag))

stage = Path(os.environ.get("TMPDIR", "/tmp")) / "context-carveouts-review"
stage.mkdir(exist_ok=True)
for rule, checks in rule_checks.items():
    for name in {n for n, _ in checks}:
        # Stage outside testdata/: several composites exclude test-directory
        # paths, so fixtures must be evaluated under a neutral path (names
        # preserved, since some exclusions are filename-based).
        staged = stage / name
        staged.write_bytes((HERE / name).read_bytes())
        result = subprocess.run(
            [os.environ.get("CLEAVE", "cleave"), "test-rules",
             "--rules", rule, str(staged)],
            capture_output=True, text=True, env=ENV,
        )
        matched = "1 matched, 0 not matched" in result.stdout
        for check_name, want in checks:
            if check_name != name:
                continue
            if want and not matched:
                failures.append(f"{name}: test-rules expected match missing: {rule}")
            if not want and matched:
                failures.append(f"{name}: test-rules unexpected match: {rule}")

if failures:
    raise SystemExit("FAIL\n" + "\n".join(failures))
print(f"PASS: {len(cases)} cases")
