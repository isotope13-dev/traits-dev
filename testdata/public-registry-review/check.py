#!/usr/bin/env python3
"""Static regression controls; no fixture code is executed or fetched."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
SCRATCH = Path(os.environ.get("REVIEW_SCRATCH", ROOT))
CASES = json.loads(Path(__file__).with_name("cases.json").read_text())


def main():
    with tempfile.TemporaryDirectory(prefix="registry-controls-", dir=SCRATCH) as tmp:
        for case in CASES:
            source = ROOT / case["path"]
            target = Path(tmp) / source.name
            shutil.copyfile(source, target)
            cmd = ["cleave", "--no-update-check", "--traits-dir", str(ROOT),
                   "--format", "json", str(target)]
            run = subprocess.run(cmd, capture_output=True, text=True, check=True)
            report = json.loads(run.stdout)
            traits = {t["id"]: t for f in report["files"] for t in f.get("traits", [])}
            for ident in case.get("require", []):
                assert ident in traits, (source.name, "missing", ident)
            for ident in case.get("forbid", []):
                assert ident not in traits, (source.name, "unexpected", ident)
            for ident, crit in case.get("severity", {}).items():
                assert traits.get(ident, {}).get("crit") == crit, (source.name, ident, traits.get(ident))
            if "max_crit" in case:
                assert all(t["crit"] <= case["max_crit"] for t in traits.values()), (
                    source.name, [(i, t["crit"]) for i, t in traits.items() if t["crit"] > case["max_crit"]])
            print("PASS", source.name)
    print(f"{len(CASES)} static regression controls passed")


if __name__ == "__main__":
    main()
