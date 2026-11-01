# /// script
# dependencies = ["pyyaml"]
# ///
"""Verify host-profile moves, removed synthetic inputs and capacity."""
from collections import Counter
import json
from pathlib import Path
import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
review = json.loads((HERE / "moves.json").read_text())
moves = review["moves"]
moves += json.loads((HERE / "refinement.json").read_text())["moves"]
renames = {m["old"]: m["new"] for m in moves}


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
    rule = next(r for r in doc[move["kind"]] if r["id"] == name)
    before = {**move["defaults"], **move["before"]}
    after = {**(doc.get("defaults") or {}), **rule}
    before.pop("id")
    after.pop("id")
    if name == "php-server-env-json-body":
        before.pop("attack", None)
        before["crit"] = "component"
        before.pop("desc", None)
        after.pop("desc", None)
    assert normalize(before, move["old"].split("::")[0]) == normalize(after, namespace), move["old"]
for removed in review["removed"]:
    assert not (ROOT / removed["path"]).exists(), removed["path"]
for retained in review.get("reviewed_retained", []):
    doc = yaml.safe_load((ROOT / retained["source"]).read_text())
    name = retained["id"].split("::")[-1]
    rule = next(r for r in doc["composite_rules"] if r["id"] == name)
    assert (doc.get("defaults") or {}) == retained["defaults"]
    assert rule == retained["rule"], retained["id"]

php = yaml.safe_load((ROOT / "objectives/exfiltration/stealer/system-info/profile/php-profile-stage.yaml").read_text())
php_rules = {rule["id"]: rule for rule in php["composite_rules"]}
for name in ("php-obfuscated-server-profile-exfil", "php-server-profile-remote-stage"):
    assert "micro-behaviors/communications/http/request/body/construction::php-server-env-json-body" in {
        condition.get("id") for condition in php_rules[name]["all"]
    }

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
directories = {str(Path(m["destination"]).parent) for m in moves}
directories.update(("objectives/exfiltration/stealer/system-info/profile", "objectives/exfiltration/stealer/system-info/identity"))
for directory in sorted(directories):
    print(f"{directory}: {physical[directory]} physical, {namespaces[directory]} namespace")
    assert physical[directory] < 72 and namespaces[directory] < 72, directory
print(f"Verified {len(moves)} rule moves and {len(review['removed'])} synthetic-file removals")
