"""Check behavior boundaries without executing fixture source."""
import json
import os
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[3]
cases = json.loads(Path(__file__).with_name("cases.json").read_text())["fixtures"]
paths = [str(root / case["path"]) for case in cases]
result = subprocess.run([os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(root),
                         "--format", "json", "--min-crit", "component", *paths], capture_output=True, text=True)
if result.returncode:
    raise SystemExit(result.stderr or result.stdout)
decoder = json.JSONDecoder()
remaining = result.stdout.strip()
reports = []
while remaining:
    item, end = decoder.raw_decode(remaining)
    reports.append(item)
    remaining = remaining[end:].lstrip()
report = {"files": [f for r in reports for f in r["files"]]}
for case, path in zip(cases, paths):
    files = [f for f in report["files"] if f["path"] == path]
    assert len(files) == 1, (path, [f["path"] for f in report["files"]])
    matched = {t["id"] for t in files[0].get("traits", [])}
    missing = set(case.get("matched", [])) - matched
    unexpected = set(case.get("not_matched", [])) & matched
    assert not missing and not unexpected, (case["path"], sorted(missing), sorted(unexpected))
    # Baseline vocabulary traits may match but be stripped unless a composite
    # references them. Check their evaluator result separately from emission.
    debug = case.get("debug_matched", []) + case.get("debug_not_matched", [])
    if debug:
        traced = subprocess.run([os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(root),
                                 "test-rules", path, "--rules", ",".join(debug)],
                                capture_output=True, text=True, check=True)
        for rule in debug:
            did_match = "\nMATCHED " + rule + " (" in "\n" + traced.stdout
            assert did_match == (rule in case.get("debug_matched", [])), (path, rule, traced.stdout)
    print(case["path"] + ": PASS")
if result.stderr:
    print(result.stderr)
