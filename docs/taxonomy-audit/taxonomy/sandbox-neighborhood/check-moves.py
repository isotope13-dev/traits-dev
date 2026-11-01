# /// script
# dependencies = ["pyyaml"]
# ///
"""Check migrated rule definitions and destination capacity."""
import json
from collections import Counter
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
moves = []
for name in ("moves.json", "second-moves.json", "third-moves.json", "fourth-moves.json"):
    moves.extend(json.loads((HERE / name).read_text())["moves"])
renames = {move["old"]: move["new"] for move in moves}
locations = {move["new"]: move["destination"] for move in moves}


def final_id(item):
    while item in renames:
        item = renames[item]
    return item


def normalize(value, namespace):
    if isinstance(value, list):
        return [normalize(item, namespace) for item in value]
    if not isinstance(value, dict):
        return value
    result = {}
    for key, item in value.items():
        # Descriptions and attack labels were reviewed separately; see README.
        if key in ("desc", "attack", "mbc"):
            continue
        if key == "id" and isinstance(item, str):
            if "/" not in item and "::" not in item:
                item = namespace + "::" + item
            result[key] = final_id(item)
        else:
            result[key] = normalize(item, namespace)
    return result


for move in moves:
    final = final_id(move["new"])
    document = yaml.safe_load((ROOT / locations[final]).read_text())
    namespace, name = final.split("::")
    rule = next(rule for kind in ("traits", "composite_rules")
                for rule in document.get(kind, []) or [] if rule["id"] == name)
    before = {**move["defaults"], **move["rule"]}
    after = {**(document.get("defaults") or {}), **rule}
    before.pop("id")
    after.pop("id")
    assert normalize(before, move["old"].split("::")[0]) == normalize(after, namespace), move["old"]

destinations = {Path(locations[final_id(move["new"])]).parent for move in moves}
destinations.update(Path("objectives/anti-analysis/sandbox-detect") / name
                    for name in ("suite", "script"))
namespaces = Counter()
for branch in ("metadata", "micro-behaviors", "objectives", "well-known"):
    for path in (ROOT / branch).rglob("*.yaml"):
        document = yaml.load(path.read_text(), Loader=yaml.CSafeLoader) or {}
        default = str(path.parent.relative_to(ROOT))
        for kind in ("traits", "composite_rules"):
            for rule in document.get(kind, []) or []:
                name = rule["id"]
                namespaces[name.split("::")[0] if "::" in name else default] += 1
for directory in sorted(destinations):
    count = 0
    for path in (ROOT / directory).glob("*.yaml"):
        document = yaml.safe_load(path.read_text()) or {}
        count += sum(len(document.get(kind) or []) for kind in ("traits", "composite_rules"))
    namespace_count = namespaces[str(directory)]
    print(f"{directory}: {count} physical, {namespace_count} in namespace")
    assert count < 72, f"{directory}: {count} rules; review and split at 72"
    assert namespace_count < 72, f"{directory}: {namespace_count} namespace rules; split at 72"

print(f"Preserved predicates, scope, severity and confidence for {len(moves)} rules")
