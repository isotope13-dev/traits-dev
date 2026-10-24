"""Static rule controls; stage outside testdata so fixture suppressions cannot hide matches."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument("--scratch", type=Path, required=True)
parser.add_argument("--cleave", default="cleave")
args = parser.parse_args()
here = Path(__file__).resolve().parent
root = here.parents[1]
cases = json.loads((here / "cases.json").read_text())
args.scratch.mkdir(parents=True, exist_ok=True)
with tempfile.TemporaryDirectory(prefix="version-drift-", dir=args.scratch) as tmp:
    paths = []
    for case in cases:
        target = Path(tmp) / case["file"]
        shutil.copyfile(here / case["file"], target)
        paths.append(str(target))
    result = subprocess.run(
        [args.cleave, "--traits-dir", str(root), "--format", "json", *paths],
        capture_output=True, text=True,
    )
    if result.returncode:
        raise RuntimeError(result.stderr)
    reports = {}
    remaining = result.stdout
    decoder = json.JSONDecoder()
    while remaining.strip():
        report, end = decoder.raw_decode(remaining.lstrip())
        remaining = remaining.lstrip()[end:]
        for file in report["files"]:
            reports[file["path"]] = {trait["id"] for trait in file.get("traits", [])}
    for case, path in zip(cases, paths):
        matched = reports[path]
        missing = set(case["required"]) - matched
        unexpected = set(case["forbidden"]) & matched
        assert not missing and not unexpected, (case["file"], missing, unexpected)
        print(case["file"], "PASS")
