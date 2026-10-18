"""Focused taxonomy and capability controls; never executes fixture code."""
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
CASES = Path(__file__).with_name("cases.json")


def main():
    cases = json.loads(CASES.read_text())["fixtures"]
    for case in cases:
        result = subprocess.run(
            [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
             "--format", "json", case["path"]],
            cwd=ROOT, text=True, capture_output=True, check=True,
        )
        report = json.loads(result.stdout)
        traits = [trait for file in report["files"] for trait in file.get("traits", [])]
        ids = {trait["id"] for trait in traits}
        missing = set(case.get("matched", [])) - ids
        unexpected = set(case.get("not_matched", [])) & ids
        assert not missing and not unexpected, (case["path"], missing, unexpected)
        if case.get("no_hostile"):
            assert not any(trait["crit"] == 5 for trait in traits), case["path"]
        print("PASS", case["path"], flush=True)
    print(f"{len(cases)} focused controls passed")


if __name__ == "__main__":
    main()
