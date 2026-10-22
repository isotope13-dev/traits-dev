#!/usr/bin/env python3
"""Check SSI capability/attack separation and alert source-shape boundaries."""
import concurrent.futures
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
CASES = json.loads((HERE / "cases.json").read_text())

def check(case):
    path = ROOT / case["path"] if "path" in case else HERE / case["file"]
    proc = subprocess.run(
        ["cleave", "--traits-dir", str(ROOT), "--format", "json", str(path)],
        capture_output=True, text=True, check=True, cwd=ROOT,
    )
    report = json.loads(proc.stdout)
    traits = {t["id"]: t["crit"] for f in report["files"] for t in f.get("traits", [])}
    for trait, severity in case["required"].items():
        assert traits.get(trait) == severity, (case["file"], trait, traits)
    if case.get("matched"):
        debug = subprocess.run(
            ["cleave", "--traits-dir", str(ROOT), "test-rules", str(path),
             "--rules", ",".join(case["matched"])],
            capture_output=True, text=True, check=True, cwd=ROOT,
        ).stdout
        for trait in case["matched"]:
            assert "MATCHED " + trait + " (" in debug, (case["file"], debug)
    for trait in case["forbidden"]:
        assert trait not in traits, (case["file"], trait)
    assert "objectives/execution/exploit/markup::ssi-exec-cmd-directive" not in traits
    return case["file"]

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    for name in pool.map(check, CASES):
        print("PASS", name)
