"""Replay controls outside testdata so intentional harness exclusions do not fire."""
import argparse
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--cleave", required=True)
parser.add_argument("--scratch", required=True)
args = parser.parse_args()
cases = json.loads(Path(__file__).with_name("cases.json").read_text())["fixtures"]
with tempfile.TemporaryDirectory(prefix="encoded-capabilities-", dir=args.scratch) as root:
    targets = []
    for case in cases:
        target = Path(root) / Path(case["path"]).name
        shutil.copyfile(case["path"], target)
        targets.append(str(target))
    output = subprocess.check_output([args.cleave, "--traits-dir", ".", "--format", "json", "analyze", *targets], text=True)
    decoder = json.JSONDecoder()
    for case in cases:
        report, end = decoder.raw_decode(output.lstrip())
        output = output.lstrip()[end:]
        matched = {trait["id"] for trait in report["files"][0]["traits"]}
        assert set(case["matched"]) <= matched, case
        assert not set(case["not_matched"]) & matched, case
print("All eight positive and negative controls passed")
