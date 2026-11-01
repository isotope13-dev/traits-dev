# /// script
# dependencies = ["pyyaml"]
# ///
"""Verify the file-exfiltration neighborhood review."""
from collections import Counter
import json
from pathlib import Path
import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
review = json.loads((HERE / "file-reorganization.json").read_text())
renames = {move["old"]: move["new"] for move in review["moves"]}


def normalize(value, namespace):
    if isinstance(value, list):
        return [normalize(item, namespace) for item in value]
    if not isinstance(value, dict):
        return value
    result = {}
    for key, item in value.items():
        if key == "desc":
            continue
        if key == "id" and isinstance(item, str):
            if "/" not in item and "::" not in item:
                item = namespace + "::" + item
            result[key] = renames.get(item, item)
        else:
            result[key] = normalize(item, namespace)
    return result


for move in review["moves"]:
    doc = yaml.safe_load((ROOT / move["destination"]).read_text()) or {}
    namespace, name = move["new"].split("::")
    rule = next(rule for rule in doc[move["kind"]] if rule["id"] == name)
    before = {**move["defaults"], **move["before"]}
    after = {**(doc.get("defaults") or {}), **rule}
    before.pop("id")
    after.pop("id")
    if name == "macos-credential-targeting-authentication":
        before["crit"] = "suspicious"
    if name == "file-read-and-transform-request":
        before["crit"] = "notable"
        before.pop("attack", None)
        before.pop("mbc", None)
    assert normalize(before, move["old"].split("::")[0]) == normalize(after, namespace), move["old"]

for removed in review["removed"]:
    assert not (ROOT / removed["path"]).exists(), removed["path"]

consumer = yaml.safe_load((ROOT / review["directory_reference_review"][0]["file"]).read_text())
rule = next(r for r in consumer["composite_rules"] if r["id"] == "python-profiled-http-collector")
ids = {item.get("id") for item in rule["any"]}
assert rule["needs"] == 3
assert set(review["directory_reference_review"][0]["added"]) <= ids
assert set(review["directory_reference_review"][0]["already_covered"]) <= ids

physical = Counter()
namespaces = Counter()
current_ids = set()
for branch in ("metadata", "micro-behaviors", "objectives", "well-known"):
    for path in (ROOT / branch).rglob("*.yaml"):
        doc = yaml.load(path.read_text(), Loader=yaml.CSafeLoader) or {}
        directory = str(path.parent.relative_to(ROOT))
        for kind in ("traits", "composite_rules"):
            for rule in doc.get(kind, []) or []:
                physical[directory] += 1
                name = rule["id"]
                qualified = name if "::" in name else directory + "::" + name
                namespaces[qualified.split("::")[0]] += 1
                if rule.get("crit", (doc.get("defaults") or {}).get("crit")) != "exception":
                    current_ids.add(qualified)

# Reconstruct the consumer's selected cohort before the moves. The removed
# QNX and unsupported non-transfer findings are deliberately excluded.
before_ids = (current_ids - set(renames.values())) | set(renames)
added = set(review["directory_reference_review"][0]["added"])
excluded = {
    "objectives/exfiltration/stealer/file::qnx-native-home-list-exfil",
    "objectives/exfiltration/stealer/system-info/identity::qnx-native-host-profile-exfil",
    "objectives/exfiltration/stealer/file::credential-stealer-macos",
    "objectives/exfiltration/stealer/file::skill-override-bulk-log-forwarding",
    "objectives/exfiltration/stealer/file::python-source-upload-to-transform-service",
}


def selected(references, population):
    result = set()
    for reference in references:
        if "::" in reference:
            result.add(reference)
        else:
            prefix = reference.rstrip("/")
            result.update(item for item in population
                          if item.startswith(prefix + "::") or item.startswith(prefix + "/"))
    return result


previous = selected(ids - added, before_ids) - excluded
expected = {renames.get(item, item) for item in previous}
actual = selected(ids, current_ids)
assert expected == actual, f"Consumer cohort changed: missing={sorted(expected - actual)}, added={sorted(actual - expected)}"
destinations = {str(Path(move["destination"]).parent) for move in review["moves"]}
destinations.update(("objectives/exfiltration/stealer/file", "objectives/exfiltration/stealer/system-info/identity"))
for directory in sorted(destinations):
    print(f"{directory}: {physical[directory]} physical, {namespaces[directory]} namespace")
    assert physical[directory] < 72 and namespaces[directory] < 72, directory
print(f"Verified {len(review['moves'])} moves, {len(review['removed'])} removals and the directory consumer")
