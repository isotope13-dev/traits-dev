"""Check trait relocations, neutral clients and preserved JWT attack detection."""
import argparse
import json
import os
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("--report", type=Path)
args = parser.parse_args()
fixture_dir = Path(__file__).resolve().parent
repo = fixture_dir.parents[2]
cases = json.loads((fixture_dir / "cases.json").read_text())
if args.report:
    output = args.report.read_text()
else:
    env = dict(os.environ, CLEAVE_SKIP_CACHE="1", CLEAVE_NO_UPDATE_CHECK="1")
    output = subprocess.run(
        [env.get("CLEAVE", "cleave"), "--traits-dir", str(repo),
         "--format", "json", str(fixture_dir)],
        env=env, cwd=repo, check=True, capture_output=True, text=True,
    ).stdout
reports = {}
decoder = json.JSONDecoder()
offset = 0
while offset < len(output):
    while offset < len(output) and output[offset].isspace():
        offset += 1
    if offset == len(output):
        break
    result, offset = decoder.raw_decode(output, offset)
    for file in result.get("files", []):
        path = Path(file["path"])
        if not path.is_absolute():
            path = repo / path
        reports[path.resolve()] = {t["id"]: t["crit"] for t in file.get("traits", [])}
for case in cases["fixtures"]:
    traits = reports[(repo / case["path"]).resolve()]
    for rule in case["matched"]:
        assert rule in traits, (case["path"], "missing", rule)
        expected_level = 5 if rule.startswith("objectives/") else 3
        assert traits[rule] == expected_level, (case["path"], rule, traits[rule])
    for rule in case["not_matched"]:
        assert rule not in traits, (case["path"], "unexpected", rule)
    if not any(rule.startswith("objectives/") for rule in case["matched"]):
        assert not any(level >= 4 for level in traits.values()), (case["path"], traits)
print(f"PASS: {len(cases['fixtures'])} cases; capability levels and JWT attack preserved")
