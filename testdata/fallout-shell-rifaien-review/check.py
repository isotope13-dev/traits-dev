"""Run static binding controls outside the scanner's test-directory exclusions."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("--scratch", required=True, type=Path)
args = parser.parse_args()
here = Path(__file__).resolve().parent
root = here.parent.parent
dest = args.scratch.resolve() / "binding-controls"
dest.mkdir(parents=True, exist_ok=True)
cases = json.loads((here / "review-cases.json").read_text())["fixtures"]
for case in cases:
    shutil.copyfile(here / case["path"], dest / case["path"])
run = subprocess.run(
    ["cleave", "--traits-dir", str(root), "analyze", "--format", "jsonl", str(dest)],
    text=True, capture_output=True, check=True,
)
reports = {}
for line in run.stdout.splitlines():
    report = json.loads(line)
    if report.get("files"):
        reports[Path(report["files"][0]["path"]).name] = report
results = []
for case in cases:
    report = reports[case["path"]]
    ids = {t["id"] for f in report["files"] for t in f.get("traits", [])}
    missing = sorted(set(case["matched"]) - ids)
    unexpected = sorted(set(case["not_matched"]) & ids)
    results.append(dict(case=case["path"], passed=not missing and not unexpected,
                        missing=missing, unexpected=unexpected))
(args.scratch / "binding-results.json").write_text(json.dumps(results, indent=2) + "\n")
assert all(row["passed"] for row in results), results
print(f"{len(results)} static controls passed")
