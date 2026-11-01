# /// script
# dependencies = ["pyyaml"]
# ///
"""Verify the object-schema split and browser-authentication migration."""
from collections import Counter
import json
from pathlib import Path
import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
schema = json.loads((HERE / "moves.json").read_text())
browser = json.loads((HERE.parent / "browser-auth-subjects/moves.json").read_text())
moves = schema["moves"] + browser["moves"]
renames = {move["old"]: move["new"] for move in moves}


def normalize(value, namespace):
    if isinstance(value, list):
        return [normalize(item, namespace) for item in value]
    if not isinstance(value, dict):
        return value
    result = {}
    for key, item in value.items():
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
    before = {**move["defaults"], **move["before"]}
    after = {**(doc.get("defaults") or {}), **rule}
    before.pop("id")
    after.pop("id")
    if move["source"].endswith("native-c2-harvest.yaml"):
        before.pop("attack", None)
        before.pop("mbc", None)
    if name in ("quoted-cookies-text", "fetch-json-bracket-body-text"):
        before.pop("desc", None)
        after.pop("desc", None)
    assert normalize(before, move["old"].split("::")[0]) == normalize(after, namespace), move["old"]

for retained in browser["retained"]:
    doc = yaml.safe_load((ROOT / retained["file"]).read_text())
    rule = next(r for r in doc[retained["kind"]] if r["id"] == retained["rule"]["id"])
    before = {**retained["defaults"], **retained["rule"]}
    after = {**(doc.get("defaults") or {}), **rule}
    if retained["file"].endswith("native-c2-harvest.yaml"):
        before.pop("attack", None)
        before.pop("mbc", None)
    namespace = str(Path(retained["file"]).parent)
    assert normalize(before, namespace) == normalize(after, namespace), retained["file"]

physical, namespaces = Counter(), Counter()
for branch in ("metadata", "micro-behaviors", "objectives", "well-known"):
    for path in (ROOT / branch).rglob("*.yaml"):
        doc = yaml.load(path.read_text(), Loader=yaml.CSafeLoader) or {}
        directory = str(path.parent.relative_to(ROOT))
        for kind in ("traits", "composite_rules"):
            for rule in doc.get(kind, []) or []:
                physical[directory] += 1
                name = rule["id"]
                namespaces[name.split("::")[0] if "::" in name else directory] += 1
directories = {str(Path(m["destination"]).parent) for m in moves}
directories.update(("micro-behaviors/data/serialize/schema-object", "micro-behaviors/data/serialize/schema-credential", "objectives/exfiltration/sensitive-data/browser"))
for directory in sorted(directories):
    print(f"{directory}: {physical[directory]} physical, {namespaces[directory]} namespace")
    assert physical[directory] < 72 and namespaces[directory] < 72, directory
print(f"Verified {len(moves)} moves and {len(browser['retained'])} retained rules")
