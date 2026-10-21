"""Check probe severity, neutral literal placement, and nearby non-probes."""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CLEAVE = os.environ.get("CLEAVE", "cleave")


def check(case):
    run = subprocess.run(
        [CLEAVE, "--traits-dir", str(ROOT), "--format", "json",
         str(HERE / case["path"])],
        capture_output=True, text=True, check=True,
    )
    report = json.loads(run.stdout)
    traits = {t["id"]: t["crit"] for f in report["files"]
              for t in f.get("traits", [])}
    for name, level in case["matched"].items():
        assert traits.get(name) == level, (case["path"], name, traits.get(name))
    for name in case["absent"]:
        assert name not in traits, (case["path"], name)
    assert not any(c == 5 for c in traits.values()), case["path"]
    assert sum(c == 4 for c in traits.values()) <= case["max_suspicious"], (
        case["path"], {k: v for k, v in traits.items() if v >= 4})
    return case["path"]


if __name__ == "__main__":
    cases = json.loads((HERE / "cases.json").read_text())
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        for name in pool.map(check, cases):
            print("PASS", name)
