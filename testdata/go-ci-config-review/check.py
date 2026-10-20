#!/usr/bin/env python3
"""Check structured CI/linter declarations against positives and near misses."""
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
spec = json.loads((HERE / "cases.json").read_text())
env = dict(os.environ, CLEAVE_TRAITS_DIR=str(ROOT), CLEAVE_SKIP_CACHE="1")
result = subprocess.run(
    ["atomscan", "--no-update", "--mode", "slow", "--follow=none", "-f", "json",
     *[str(HERE / case["path"]) for case in spec["cases"]]],
    env=env, capture_output=True, text=True, check=True,
)
reports = [json.loads(line) for line in result.stdout.splitlines() if line.strip()]
files = {Path(f["path"]).resolve(): f
         for report in reports for f in report["raw"]["files"]}
for case in spec["cases"]:
    report = files[(HERE / case["path"]).resolve()]
    findings = report.get("traits", [])
    ids = {t["id"] for t in findings}
    actual = ids.intersection(spec["traits"])
    assert actual == set(case["expected"]), (case["path"], actual)
    assert not any(t["crit"] >= 4 for t in findings), (case["path"], findings)
    assert not any(t["id"].startswith("well-known/tool/development/lint/linter::golangci-")
                   for t in findings), (case["path"], findings)
    print("PASS", case["path"])
