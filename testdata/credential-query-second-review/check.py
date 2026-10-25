"""Scan inert positive and near-miss controls from neutral paths."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def main():
    cases = json.loads((HERE / "cases.json").read_text())["fixtures"]
    with tempfile.TemporaryDirectory(prefix="query-controls-", dir=sys.argv[1]) as tmp:
        targets = []
        for case in cases:
            target = Path(tmp) / case["path"]
            shutil.copyfile(HERE / case["path"], target)
            targets.append(str(target))
        result = subprocess.run(
            [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
             "--format", "json", *targets], capture_output=True, text=True,
            check=True)
        source = result.stdout
        decoder = json.JSONDecoder()
        reports = {}
        while source.strip():
            report, end = decoder.raw_decode(source.lstrip())
            source = source.lstrip()[end:]
            for file in report["files"]:
                reports[file["path"]] = {t["id"] for t in file.get("traits", [])}
        failures = []
        for case, target in zip(cases, targets):
            if target not in reports:
                failures.append({"path": case["path"], "missing_report": True})
                continue
            ids = reports[target]
            missing = set(case["matched"]) - ids
            unexpected = set(case["not_matched"]) & ids
            if missing or unexpected:
                failures.append({"path": case["path"], "missing": sorted(missing),
                                 "unexpected": sorted(unexpected)})
    print(json.dumps({"cases": len(cases), "failures": failures}, indent=2))
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    return bool(failures)


if __name__ == "__main__":
    sys.exit(main())
