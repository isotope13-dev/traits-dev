"""Apply the final conservative item review to the already migrated inventory."""

import copy
import io
import json
import re
import tempfile
from collections import Counter
from pathlib import Path

from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedSeq

root = Path(__file__).parent
repo = root.resolve().parents[2]
prefix = "objectives/exfiltration/stealer"
plan = {r["old_id"]: r for r in json.loads((root / "item-placement-plan.json").read_text())}
current = json.loads((root / "item-id-map.json").read_text())
aliases = {
    prefix + "/cloud::swift-cloud-credential-http-exfil": "swift-mixed-store-credential-http-exfil",
    prefix + "/credential::swift-cloud-credential-http-exfil": "swift-cloud-file-content-http-exfil",
    prefix + "/env::env-vars": "encoded-env-secret-http-exfil",
}
desired = {old: row["new_directory"] + "::" + aliases.get(old, row["new_name"]) for old, row in plan.items() if row["new_directory"]}
assert set(desired) == set(current)
assert len(desired.values()) == len(set(desired.values()))
changes = {current[old]: desired[old] for old in desired if current[old] != desired[old]}
if not changes:
    print("The current IDs already match the reviewed item plan.")
    raise SystemExit(0)
assert not set(changes) & set(changes.values()), "Use a simultaneous node rewrite for a cyclic move"
yaml = YAML()
yaml.preserve_quotes = True
yaml.width = 120
docs = {}
texts = {}
locations = {}
definitions = set()
for directory in sorted({full.split("::")[0] for full in (*current.values(), *desired.values())}):
    for path in sorted((repo / directory).glob("*.yaml")):
        rel = str(path.relative_to(repo))
        doc = yaml.load(path.read_text())
        docs[rel] = doc
        texts[rel] = path.read_text()
        for kind in ("traits", "composite_rules"):
            for rule in doc.get(kind, []) or []:
                full = directory + "::" + rule["id"]
                assert full not in definitions, full
                definitions.add(full)
                if full in changes:
                    locations[full] = (rel, kind, rule)
assert set(locations) == set(changes)
assert not (set(changes.values()) & (definitions - set(changes)))
dirty = set()


def refs(value, parent, qualify_all=False):
    changed = False
    if isinstance(value, dict):
        for key, child in list(value.items()):
            if key == "id" and isinstance(child, str):
                bare = "/" not in child and "::" not in child
                full = parent + "::" + child if bare else child
                if full in changes:
                    value[key] = changes[full]
                    changed = True
                elif bare and qualify_all and full in definitions:
                    value[key] = full
                    changed = True
            elif key != "id":
                changed = refs(child, parent, qualify_all) or changed
    elif isinstance(value, list):
        for child in value:
            changed = refs(child, parent, qualify_all) or changed
    return changed


# Resolve bare references in every affected ancestor population, including
# consumers in other files of the same current directory.
for rel, doc in docs.items():
    parent = str(Path(rel).parent)
    for kind in ("traits", "composite_rules"):
        for rule in doc.get(kind, []) or []:
            moving = parent + "::" + rule["id"] in changes
            for key, value in list(rule.items()):
                if key != "id" and refs(value, parent, moving):
                    dirty.add(rel)

new_docs = {}
reverse_current = {value: old for old, value in current.items()}
descriptions = {
    "lua-unix-sensitive-file-path-set": "References a set of Unix sensitive file paths",
    "netscaler-config-secret-source-references": "References NetScaler configuration, secret paths and user API",
    "routeros-user-list-dump-context": "Reads a RouterOS user listing into a named dump value",
    "rust-routeros-secret-config-path-set": "References RouterOS secret and backup configuration paths",
    "ahk-error-send-body": "Sends the literal v=e! diagnostic body",
    "powershell-joined-output-post-body": "Passes joined output to a POST helper",
    "node-feature-gated-file-read": "A workflow-sync feature flag gates whole-file reading",
    "node-marker-gated-post": "A marker check precedes an HTTP POST",
}
for old, new in changes.items():
    rel, kind, rule = locations[old]
    source_doc = docs[rel]
    target, name = new.split("::")
    moved = copy.deepcopy(rule)
    moved["id"] = name
    if name in descriptions:
        moved["desc"] = descriptions[name]
    if target.startswith(("micro-behaviors/", "metadata/")):
        moved["crit"] = "notable"
        moved.pop("attack", None)
        moved.pop("mbc", None)
    new_doc = copy.deepcopy(source_doc)
    for group in ("traits", "composite_rules"):
        new_doc.pop(group, None)
    new_doc[kind] = CommentedSeq([moved])
    if target.startswith(("micro-behaviors/", "metadata/")):
        defaults = new_doc.get("defaults", {})
        defaults.pop("attack", None)
        defaults.pop("mbc", None)
    destination = target + "/item-" + name + ".yaml"
    assert not (repo / destination).exists(), destination
    assert destination not in new_docs
    new_docs[destination] = new_doc
    source_doc[kind].remove(rule)
    if not source_doc[kind]:
        source_doc.pop(kind)
    dirty.add(rel)

pattern = re.compile("(?:" + "|".join(re.escape(k) for k in sorted(changes, key=len, reverse=True)) + r")(?![A-Za-z0-9_-])")
pending = {}
for rel in dirty:
    doc = docs[rel]
    if not any(doc.get(kind) for kind in ("traits", "composite_rules")):
        pending[rel] = None
    else:
        stream = io.StringIO()
        yaml.dump(doc, stream)
        pending[rel] = pattern.sub(lambda m: changes[m.group()], stream.getvalue())
for rel, doc in new_docs.items():
    stream = io.StringIO()
    yaml.dump(doc, stream)
    pending[rel] = pattern.sub(lambda m: changes[m.group()], stream.getvalue())
for tier in ("micro-behaviors", "objectives", "metadata", "well-known"):
    for path in (repo / tier).rglob("*.yaml"):
        rel = str(path.relative_to(repo))
        if rel in pending:
            continue
        before = path.read_text()
        after = pattern.sub(lambda m: changes[m.group()], before)
        if after != before:
            pending[rel] = after
expectations = "testdata/expectations.toml"
before = (repo / expectations).read_text()
after = pattern.sub(lambda m: changes[m.group()], before)
if after != before:
    pending[expectations] = after

backup = Path(tempfile.mkdtemp(prefix="stealer-item-final-review-"))
for rel in pending:
    path = repo / rel
    if path.exists():
        dest = backup / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(path.read_text())
for rel, text in pending.items():
    path = repo / rel
    if text is None:
        path.unlink()
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

(root / "item-id-map.json").write_text(json.dumps(desired, indent=2) + "\n")
audit = json.loads((root / "item-placement-audit.json").read_text())
history = audit.setdefault("final_review_history", [])
if not history and audit.get("final_review_backup"):
    prior_map = root / "item-final-review-map.json"
    history.append({"backup": audit["final_review_backup"], "changes": json.loads(prior_map.read_text())})
history.append({"backup": str(backup), "changes": changes})
for row in audit["rules"]:
    old = row["old_id"]
    row["new_id"] = desired.get(old)
    row["reason"] = plan[old]["reason"]
    row["action"] = "remove-unsupported-claim" if old not in desired else "retain" if old == desired[old] else "move"
    if current.get(old) in changes:
        row["final_item_review"] = "The full predicate review refined the item type or removed a source-only observation from the theft tier."
counts = Counter(full.split("::")[0] for full in desired.values())
counts[prefix + "/configuration/environment"] += 1
audit["counts"] = dict(counts)
audit["final_review_backup"] = str(backup)
(root / "item-placement-audit.json").write_text(json.dumps(audit, indent=2) + "\n")
(root / "item-final-review-map.json").write_text(json.dumps(changes, indent=2) + "\n")
print("final item refinements", len(changes), "backup", backup)
for directory, count in sorted(counts.items()):
    if count > 100:
        print("REVIEWED BUDGET", count, directory)
