import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

root = Path(__file__).resolve().parents[3]
cases = json.loads(Path(__file__).with_name("cases.json").read_text())
engine = os.environ.get("CLEAVE", "cleave")
with tempfile.TemporaryDirectory(prefix="mining-controls-") as tmp:
    for case in cases["fixtures"]:
        target = Path(tmp) / Path(case["path"]).name
        shutil.copyfile(root / case["path"], target)
        result = subprocess.run([engine, "--traits-dir", str(root), "--format", "json", str(target)], capture_output=True, text=True, check=True)
        report = json.loads(result.stdout)
        traits = {t["id"]: t for f in report["files"] for t in f["traits"]}
        for trait in case["matched"]:
            assert trait in traits, (case["case_id"], "missing", trait)
            assert traits[trait]["crit"] == 3, (trait, "must be notable")
        for trait in case["not_matched"]:
            assert trait not in traits, (case["case_id"], "unexpected", trait)
        print("PASS", case["case_id"])
