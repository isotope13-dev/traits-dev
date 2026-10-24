#!/usr/bin/env python3
"""Exercise refusal semantics without inheriting test-directory exclusions."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("--cleave", default="cleave")
parser.add_argument("--scratch-dir", type=Path, required=True)
args = parser.parse_args()
repo = Path(__file__).resolve().parents[3]
cases = json.loads(Path(__file__).with_name("cases.json").read_text())["fixtures"]
args.scratch_dir.mkdir(parents=True, exist_ok=True)
paths = []
for case in cases:
    source = repo / case["path"]
    target = args.scratch_dir / source.name
    shutil.copyfile(source, target)
    paths.append(str(target))
result = subprocess.run(
    [args.cleave, "--traits-dir", str(repo), "--json", *paths],
    check=True, capture_output=True, text=True,
)
reports = [json.loads(line) for line in result.stdout.splitlines() if line.strip()]
findings = {
    Path(file["path"]).name: {trait["id"] for trait in file.get("traits", [])}
    for report in reports for file in report["files"]
}
for case in cases:
    name = Path(case["path"]).name
    actual = findings[name]
    missing = set(case["matched"]) - actual
    unexpected = set(case["not_matched"]) & actual
    assert not missing and not unexpected, (name, missing, unexpected)
    print(f"PASS {name}")
