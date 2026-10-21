"""Static controls copied outside testdata so path exclusions cannot hide errors."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("--work-dir", type=Path, required=True)
args = parser.parse_args()
here = Path(__file__).resolve().parent
root = here.parents[2]
cases = json.loads((here / "cases.json").read_text())
args.work_dir.mkdir(parents=True, exist_ok=True)
for name in cases:
    shutil.copyfile(here / name, args.work_dir / name)
result = subprocess.run(
    ["cleave", "--traits-dir", str(root), "--format", "json", str(args.work_dir)],
    text=True, capture_output=True, check=True,
)
assert not result.stderr.strip(), result.stderr
remaining = result.stdout
seen = set()
decoder = json.JSONDecoder()
while remaining.strip():
    report, end = decoder.raw_decode(remaining.lstrip())
    remaining = remaining.lstrip()[end:]
    for file in report["files"]:
        name = Path(file["path"]).name
        case = cases[name]
        traits = {t["id"]: t["crit"] for t in file.get("traits", [])}
        assert set(case.get("matched", [])) <= traits.keys(), (name, traits)
        assert not set(case.get("not_matched", [])) & traits.keys(), (name, traits)
        assert all(c < 5 for c in traits.values()), (name, traits)
        assert sum(c == 4 for c in traits.values()) == case["suspicious"], (name, traits)
        seen.add(name)
assert seen == cases.keys(), seen
print(f"Passed {len(seen)} static controls")
