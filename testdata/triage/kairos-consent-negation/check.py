#!/usr/bin/env python3
"""Check consent prohibitions and independent concealed directives."""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
CASES = json.loads(Path(__file__).with_name("cases.json").read_text())["fixtures"]

def check(case):
    result = subprocess.run(
        [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
         "--format", "json", str(ROOT / case["path"])],
        capture_output=True, text=True,
        env=dict(os.environ, CLEAVE_VALIDATE="0"),
    )
    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout)
    seen = {t["id"] for f in report["files"] for t in f.get("traits", [])}
    assert all(t in seen for t in case["matched"]), case["path"]
    assert all(t not in seen for t in case["not_matched"]), case["path"]
    return Path(case["path"]).name

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    for name in pool.map(check, CASES):
        print(name + ": passed")
