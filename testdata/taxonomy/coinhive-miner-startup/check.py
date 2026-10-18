#!/usr/bin/env python3
"""Check mining capabilities, consent controls, and concealed-miner regressions."""
import json
import os
from pathlib import Path
import subprocess


root = Path(__file__).resolve().parents[3]
cases = json.loads(Path(__file__).with_name("cases.json").read_text())["fixtures"]
for case in cases:
    result = subprocess.run(
        [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(root),
         "--format", "json", str(root / case["path"])],
        check=True, capture_output=True, text=True,
    )
    traits = {
        trait["id"]: trait
        for file in json.loads(result.stdout)["files"]
        for trait in file.get("traits", [])
    }
    missing = set(case["matched"]) - traits.keys()
    unexpected = set(case["not_matched"]) & traits.keys()
    assert not missing, (case["case_id"], "missing", missing)
    assert not unexpected, (case["case_id"], "unexpected", unexpected)
    if "max_crit" in case:
        assert all(t["crit"] <= case["max_crit"] for t in traits.values()), (
            case["case_id"], "unexpected severity", traits,
        )
    else:
        assert all(traits[tid]["crit"] == 5 for tid in case["matched"]), (
            case["case_id"], "concealed-miner severity changed",
        )
    print("PASS", case["case_id"])
