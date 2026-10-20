"""Static-only regression checks; fixture programs are never executed."""
import concurrent.futures
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

root = Path(__file__).resolve().parents[3]
cases = json.loads(Path(__file__).with_name("cases.json").read_text())["fixtures"]
if len(sys.argv) > 1:
    cases = [case for case in cases if Path(case["path"]).name in sys.argv[1:]]
engine = os.environ.get("CLEAVE", "cleave")
exception = "micro-behaviors/ui/help::text-only-shell-template-reference"

def check(case, directory):
    # Exercise content under neutral paths: test-directory exclusions must not
    # hide the behaviors these cases are supposed to verify.
    artifact = Path(directory) / Path(case["path"]).name
    shutil.copyfile(root / case["path"], artifact)
    result = subprocess.run(
        [engine, "--format", "json", str(artifact)],
        cwd=root, text=True, capture_output=True, check=True,
    )
    report = json.loads(result.stdout)
    findings = [t for f in report["files"] for t in f.get("traits", [])]
    emitted = {t["id"] for t in findings}
    required = set(case["matched"]) - {exception}
    assert required <= emitted, (case["path"], required - emitted)
    assert not emitted.intersection(case["forbidden_emitted"]), case["path"]
    if "max_crit" in case:
        assert all(t["crit"] <= case["max_crit"] for t in findings), case["path"]
    if exception in case["matched"] + case["not_matched"]:
        debug = subprocess.run(
            [engine, "test-rules", str(artifact), "--rules", exception],
            cwd=root, text=True, capture_output=True, check=True,
        )
        matched = bool(re.search(r"^MATCHED " + re.escape(exception), debug.stdout, re.M))
        assert matched == (exception in case["matched"]), debug.stdout + debug.stderr
    print("PASS", case["path"], flush=True)

with tempfile.TemporaryDirectory(prefix="trait-controls-", dir=root) as directory:
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        list(executor.map(lambda case: check(case, directory), cases))
print(f"{len(cases)} static regression cases passed")
