"""Check match boundaries on copies outside test-directory exclusions."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument("--scratch", type=Path, required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parents[3]
env = dict(os.environ, CLEAVE_TRAITS_DIR=str(root), SCAN_NO_UPDATE="1")
suites = [Path(__file__).parent, root / "testdata/taxonomy/python-fragment-list-mod4",
          root / "testdata/taxonomy/ccxt-version-drift"]
with tempfile.TemporaryDirectory(prefix="elevenlabs-controls-", dir=args.scratch) as neutral:
    for suite in suites:
        for case in json.loads((suite / "cases.json").read_text())["fixtures"]:
            source = root / case["path"] if case["path"].startswith("testdata/") else suite / case["path"]
            target = Path(neutral) / source.name
            shutil.copyfile(source, target)
            result = subprocess.run(["cleave", "--traits-dir", str(root), "--format", "json", str(target)],
                                    env=env, capture_output=True, text=True, check=True)
            report = json.loads(result.stdout)
            matched = {trait["id"] for file in report["files"] for trait in file.get("traits", [])}
            missing = set(case["matched"]) - matched
            unexpected = set(case["not_matched"]) & matched
            assert not missing and not unexpected, (source.name, missing, unexpected)
            print(f"PASS {source.name}", flush=True)
