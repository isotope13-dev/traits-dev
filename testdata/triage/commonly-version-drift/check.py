"""Check saved cleave JSONL reports, including before/after attack retention."""
import argparse
import json
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--before", action="append", type=Path, required=True)
parser.add_argument("--after", action="append", type=Path, required=True)
args = parser.parse_args()


def reports(paths):
    result = {}
    for path in paths:
        for line in path.read_text().splitlines():
            report = json.loads(line)
            report = report.get("raw", report)
            root = report["files"][0]
            result[Path(root["path"]).name] = report
    return result


before = reports(args.before)
after = reports(args.after)
cases = json.loads(Path(__file__).with_name("cases.json").read_text())
for name, expected in cases.items():
    assert name in after, f"missing report: {name}"
    traits = {t["id"] for t in after[name]["files"][0].get("traits", [])}
    assert set(expected["required"]) <= traits, (name, "missing", set(expected["required"]) - traits)
    assert not set(expected["forbidden"]) & traits, (name, "unexpected", set(expected["forbidden"]) & traits)

clone = "objectives/supply-chain/impersonation/clone-and-rename::npm-monorepo-readme-clone-publish-burst"
checked = 0
for name in before.keys() & after.keys():
    def attacks(report):
        return {(t["id"], t["crit"]) for f in report["files"]
                for t in f.get("traits", []) if t["crit"] >= 4}

    lost = attacks(before[name]) - attacks(after[name])
    allowed = {(clone, 4)} if name == "product-title.tgz" else set()
    assert lost <= allowed, (name, "lost attack detection", lost - allowed)
    checked += 1

print(f"PASS: {len(cases)} fixture expectations; attack retention across {checked} reports")
