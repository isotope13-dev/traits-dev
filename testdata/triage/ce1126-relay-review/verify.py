#!/usr/bin/env python3
"""Check tasking, window concealment, and neutral encoded-command controls.

Copy fixtures away from testdata so test-context exclusions cannot hide a
regression. Read and analyze code only; never execute a fixture.
"""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
CASES = json.loads(Path(__file__).with_name("cases.json").read_text())["fixtures"]

with tempfile.TemporaryDirectory(prefix=".relay-review-", dir=ROOT) as stage:
    targets = []
    for case in CASES:
        target = Path(stage) / Path(case["path"]).name
        shutil.copyfile(ROOT / case["path"], target)
        targets.append(str(target))
    result = subprocess.run(
        [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
         "--format", "jsonl", *targets],
        text=True, capture_output=True, check=True,
    )
    files = {}
    for line in result.stdout.splitlines():
        for unit in json.loads(line)["files"]:
            files[unit["path"]] = unit
    for case, target in zip(CASES, targets):
        unit = files[target]
        traits = {t["id"]: t for t in unit.get("traits", [])}
        for trait in case.get("matched", []):
            assert trait in traits, (case["path"], "missing", trait)
        for trait in case.get("not_matched", []):
            assert trait not in traits, (case["path"], "unexpected", trait)
        if case.get("no_hostile"):
            assert not any(t["crit"] == 5 for t in traits.values()), case["path"]
        for trait in (
            "micro-behaviors/process/interpreter/powershell/command::powershell-encoded-payload-command-text",
            "metadata/file/encoding::base64-utf16le-dollar-prefix",
        ):
            if trait in traits:
                assert traits[trait]["crit"] == 3, (case["path"], trait)
print(f"Passed {len(CASES)} tasking and benign controls")
