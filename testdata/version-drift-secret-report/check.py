"""Verify preserved observations/hostile controls across the source-name move.
Usage: python3 check.py before-controls.jsonl before-attack.jsonl after.jsonl
"""
import json
import sys
from pathlib import Path


def load(path):
    data = Path(path).read_text()
    decoder = json.JSONDecoder()
    reports = {}
    while data.strip():
        report, end = decoder.raw_decode(data.lstrip())
        data = data.lstrip()[end:]
        for item in report["files"]:
            reports[Path(item["path"]).name] = item
    return reports


mapping = json.loads(Path(__file__).with_name("migration.json").read_text())["mapping"]
before = load(sys.argv[1])
before.update(load(sys.argv[2]))
after = load(sys.argv[3])
for name, old in before.items():
    new = after[name]
    expected = {mapping.get(t["id"], t["id"]) for t in old.get("traits", [])}
    actual = {t["id"] for t in new.get("traits", [])}
    assert expected == actual, (name, expected - actual, actual - expected)
    hostile = lambda r: {t["id"] for t in r.get("traits", []) if t["crit"] == 5}
    assert hostile(old) == hostile(new), name
    print("PASS preserved observations and hostile detections:", name)

for name in ("scan-report.mts", "mixed-report.js", "plural-report.js", "local-derivation.js"):
    traits = after[name].get("traits", [])
    assert not any(t["crit"] >= 4 for t in traits), name
    assert any("metadata/lang/source/syntax/call/" in t["id"] for t in traits), name
    print("PASS source-name observation without inferred theft:", name)
