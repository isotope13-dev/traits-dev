# /// script
# dependencies = ["pyyaml"]
# ///
"""Check matchers, effective scope and destination populations."""
from collections import Counter
import json
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
moves = json.loads((HERE / "moves.json").read_text())["moves"]
renames = {m["old"]: m["new"] for m in moves}


def normalize(value, namespace):
    if isinstance(value, list):
        return [normalize(item, namespace) for item in value]
    if not isinstance(value, dict):
        return value
    result = {}
    for key, item in value.items():
        if key in ("desc", "crit", "attack", "mbc"):
            continue
        if key == "id" and isinstance(item, str):
            if "/" not in item and "::" not in item:
                item = namespace + "::" + item
            result[key] = renames.get(item, item)
        else:
            result[key] = normalize(item, namespace)
    return result


for move in moves:
    doc = yaml.safe_load((ROOT / move["destination"]).read_text()) or {}
    namespace, name = move["new"].split("::")
    rule = next(rule for rule in doc[move["kind"]] if rule["id"] == name)
    old = {**move["defaults"], **move["before"]}
    new = {**(doc.get("defaults") or {}), **rule}
    old.pop("id")
    new.pop("id")
    assert normalize(old, move["old"].split("::")[0]) == normalize(new, namespace), move["old"]
    assert new.get("crit") == move["criticality"], move["old"]

destinations = {Path(m["destination"]).parent for m in moves}
physical = Counter()
namespaces = Counter()
for branch in ("metadata", "micro-behaviors", "objectives", "well-known"):
    for path in (ROOT / branch).rglob("*.yaml"):
        doc = yaml.load(path.read_text(), Loader=yaml.CSafeLoader) or {}
        directory = str(path.parent.relative_to(ROOT))
        for kind in ("traits", "composite_rules"):
            for rule in doc.get(kind, []) or []:
                physical[directory] += 1
                name = rule["id"]
                namespaces[name.split("::")[0] if "::" in name else directory] += 1
for directory in sorted(map(str, destinations)):
    print(f"{directory}: {physical[directory]} physical, {namespaces[directory]} namespace")
    assert physical[directory] < 72 and namespaces[directory] < 72, directory
print(f"Verified {len(moves)} matchers and intended criticalities")
