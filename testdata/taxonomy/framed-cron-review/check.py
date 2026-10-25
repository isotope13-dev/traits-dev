"""Scan matcher controls; specimens are never executed."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

root = Path(__file__).resolve().parents[3]
cases = json.loads(Path(__file__).with_name("cases.json").read_text())
with tempfile.TemporaryDirectory(prefix=".framed-cron-controls-", dir=root) as stage:
    paths = []
    for case in cases:
        source = root / case["path"]
        if "stage_basename" in case:
            # Exercise endpoint matchers away from corpus-path suppressors.
            target = Path(stage) / case["stage_basename"]
            target.write_bytes(source.read_bytes())
            paths.append(str(target))
        else:
            paths.append(str(source))
    result = subprocess.run([os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(root),
                             "--format", "json", *paths], capture_output=True, text=True, check=True)
    stream = result.stdout.lstrip()
    reports = {}
    decoder = json.JSONDecoder()
    while stream:
        report, count = decoder.raw_decode(stream)
        stream = stream[count:].lstrip()
        reports[str(Path(report["files"][0]["path"]).resolve())] = report
    for case, path in zip(cases, paths):
        report = reports[path]
        traits = {trait["id"] for file in report["files"] for trait in file.get("traits", [])}
        for expected in case.get("present", []):
            assert expected in traits, (case["path"], "missing", expected)
        for excluded in case.get("absent", []):
            assert excluded not in traits, (case["path"], "unexpected", excluded)
        if "max_crit" in case:
            high = [trait["id"] for file in report["files"] for trait in file.get("traits", [])
                    if trait["crit"] > case["max_crit"]]
            assert not high, (case["path"], "overstated", high)
    print(json.dumps({"passed": len(cases), "specimens_executed": False}))
