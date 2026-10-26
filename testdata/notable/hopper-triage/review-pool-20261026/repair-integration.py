"""Finish reviewed placements and simplify only equivalent selector sets."""
import copy
import io
import json
import re
import tempfile
from collections import Counter, defaultdict
from pathlib import Path

from ruamel.yaml import YAML

root = Path(__file__).parent
repo = root.resolve().parents[2]
yaml = YAML()
yaml.preserve_quotes = True
yaml.width = 120
backup = Path(tempfile.mkdtemp(prefix="stealer-integration-"))
changes = {}

def write(path, text):
    before = path.read_text() if path.exists() else None
    if before == text:
        return
    rel = path.relative_to(repo)
    if before is not None:
        dest = backup / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(before)
    if text is None:
        path.unlink()
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text.rstrip() + "\n")

def dump(doc):
    stream = io.StringIO()
    yaml.dump(doc, stream)
    return stream.getvalue()

moves = {
    "micro-behaviors/communications/http/client/wallet-keyring.yaml": "micro-behaviors/communications/http/client/exchange/wallet-keyring.yaml",
    "micro-behaviors/communications/url/construction/objc-openbsd-dns.yaml": "micro-behaviors/communications/url/construction/template/objc-openbsd-dns.yaml",
    "micro-behaviors/os/package/enumerate/android-source.yaml": "micro-behaviors/os/package-manager/management/android-package-name-list.yaml",
    "micro-behaviors/fs/path/credential/item-netscaler-config-secret-source-references.yaml": "objectives/credential-access/files/appliance/netscaler-config-sources.yaml",
    "micro-behaviors/fs/path/credential/item-rust-routeros-secret-config-path-set.yaml": "objectives/credential-access/files/appliance/routeros-secret-config-sources.yaml",
}
for old, new in moves.items():
    old_path, new_path = repo / old, repo / new
    doc = yaml.load((old_path if old_path.exists() else new_path).read_text())
    for kind in ("traits", "composite_rules"):
        for rule in doc.get(kind, []) or []:
            changes[str(Path(old).parent) + "::" + rule["id"]] = str(Path(new).parent) + "::" + rule["id"]
    if old_path.exists():
        assert not new_path.exists()
        write(new_path, dump(doc))
        write(old_path, None)

changes["objectives/credential-access/theft/multi-store::batch-credential-store-source-context"] = "objectives/credential-access/theft/multi-store::batch-credential-store-indicators"
descriptions = {
    "managed-infection-type-report-field": "Managed infection-type report field",
    "serialized-wallet-keyring-payload-field": "Serialized keyring value in a payload field",
    "native-export-frame-passwd-shadow": "Export-frame labels name passwd or shadow",
    "native-export-frame-env-version": "Export-frame labels name environment or version",
    "cursor-auth-bridge-log-message": "Cursor authentication bridge log message",
    "zig-hex-label-format-reference": "Hexadecimal alphabet and formatted labels",
    "managed-telegram-session-capture-routines-reference": "Telegram session-capture routine names",
    "credentials-call-json-payload-context": "Credentials call near JSON serialization",
    "node-file-bucket-json-fields": "Environment, JSON and document bucket fields",
    "zig-resolver-credential-path-proximity": "Resolver text near credential-file paths",
    "node-feature-gated-file-read": "Workflow-sync flag gates whole-file reading",
    "agent-auth-json-raw-read": "Raw-read helper near agent auth filenames",
    "postinstall-ecs-metadata-uri-reference": "Postinstall references ECS metadata variable",
    "netscaler-config-secret-source-references": "NetScaler configuration and secret sources",
    "rust-routeros-secret-config-path-set": "RouterOS secret and backup configuration paths",
}
assert all(len(s) <= 48 and len(s.split()) <= 7 for s in descriptions.values())
hoist = {
    "objectives/exfiltration/stealer/application-state/cookie-skimmer-javascript.yaml": "mbc",
    "objectives/exfiltration/stealer/application-state/javascript.yaml": "mbc",
    "objectives/exfiltration/stealer/credential/node-unix-dev-files.yaml": "mbc",
    "objectives/exfiltration/stealer/credential/npm-ecs-metadata.yaml": "mbc",
    "objectives/exfiltration/stealer/credential/token/combos.yaml": "for",
    "objectives/exfiltration/stealer/financial/payment-card/payment-skimmer-javascript.yaml": "for",
}
paths = [p for tier in ("micro-behaviors", "objectives", "metadata", "well-known") for p in (repo / tier).rglob("*.yaml")]
pattern = re.compile("(?:" + "|".join(re.escape(k) for k in sorted(changes, key=len, reverse=True)) + r")(?![A-Za-z0-9_-])")
docs = {}
definitions = {}
for path in paths:
    text = path.read_text()
    rewritten = pattern.sub(lambda m: changes[m.group()], text)
    doc = yaml.load(rewritten) or {}
    dirty = rewritten != text
    rel = str(path.relative_to(repo))
    rules = [r for kind in ("traits", "composite_rules") for r in doc.get(kind, []) or []]
    for rule in rules:
        full = str(path.parent.relative_to(repo)) + "::" + rule["id"]
        if full in changes:  # the definition's bare name
            rule["id"] = changes[full].split("::")[1]
            dirty = True
        if rule["id"] in descriptions and rule.get("desc") != descriptions[rule["id"]]:
            rule["desc"] = descriptions[rule["id"]]
            dirty = True
        full = str(path.parent.relative_to(repo)) + "::" + rule["id"]
        assert full not in definitions, full
        definitions[full] = {**(doc.get("defaults") or {}), **rule}
    if rel in hoist:
        field = hoist[rel]
        values = [r.get(field, doc.get("defaults", {}).get(field)) for r in rules]
        assert values and all(v == values[0] for v in values)
        doc.setdefault("defaults", {})[field] = copy.deepcopy(values[0])
        for rule in rules:
            if field in rule:
                del rule[field]
                dirty = True
    docs[path] = doc
    if dirty:
        write(path, dump(doc))

# A directory selector includes rules directly in the directory AND below it.
# Only replace a list if every current member is already selected.
members = defaultdict(set)
for full in definitions:
    directory = Path(full.split("::")[0])
    for parent in (directory, *directory.parents):
        if str(parent) != ".":
            members[str(parent)].add(full)

receipts = []
for path, doc in docs.items():
    directory = str(path.parent.relative_to(repo))
    dirty = False
    for rule in doc.get("composite_rules", []) or []:
        full = directory + "::" + rule["id"]
        for clause in ("any", "unless"):
            legs = rule.get(clause)
            if not isinstance(legs, list):
                continue
            original = copy.deepcopy(legs)
            # This retired directory has no surviving export predicates.
            legs[:] = [leg for leg in legs if leg != {"id": "objectives/exfiltration/stealer/surveillance/"}]
            selected = set()
            for leg in legs:
                if isinstance(leg, dict) and set(leg) == {"id"}:
                    ref = leg["id"]
                    ref = directory + "::" + ref if "/" not in ref and "::" not in ref else ref
                    selected.update({ref} if "::" in ref else members.get(ref.rstrip("/"), set()))
            candidates = [d for d, ids in members.items() if len(ids) >= 5 and ids <= selected and not full in ids]
            # Choose maximal fully covered subtrees.
            chosen = []
            for candidate in sorted(candidates, key=lambda d: (d.count("/"), d)):
                if not any(candidate.startswith(parent + "/") for parent in chosen):
                    chosen.append(candidate)
            result = []
            seen = set()
            # Include existing selectors, so they subsume their individual legs.
            selectors = set(chosen) | {leg["id"].rstrip("/") for leg in legs if isinstance(leg, dict) and set(leg) == {"id"} and "/" in leg["id"] and "::" not in leg["id"]}
            for leg in legs:
                if isinstance(leg, dict) and set(leg) == {"id"}:
                    ref = leg["id"]
                    qualified = directory + "::" + ref if "/" not in ref and "::" not in ref else ref
                    target = qualified.split("::")[0].rstrip("/")
                    covers = sorted((s for s in selectors if target == s or target.startswith(s + "/")), key=lambda s: (s.count("/"), s))
                    if covers:
                        leg = {"id": covers[0] + "/"}
                key = json.dumps(leg, sort_keys=True)
                if key not in seen:
                    result.append(leg)
                    seen.add(key)
            if list(original) != result:
                rule[clause] = result
                dirty = True
                receipts.append({"rule": full, "clause": clause, "before": original, "after": result})
    if dirty:
        write(path, dump(doc))

for filename in ("item-id-map.json", "item-placement-plan.json", "item-placement-audit.json"):
    path = root / filename
    data = json.loads(path.read_text())
    if filename == "item-id-map.json":
        data = {old: changes.get(new, new) for old, new in data.items()}
    elif filename == "item-placement-plan.json":
        for row in data:
            full = row["new_directory"] + "::" + row["new_name"] if row["new_directory"] else None
            if full in changes:
                row["new_directory"], row["new_name"] = changes[full].split("::")
    else:
        for row in data["rules"]:
            row["new_id"] = changes.get(row["new_id"], row["new_id"])
        counts = Counter(row["new_id"].split("::")[0] for row in data["rules"] if row["new_id"])
        counts["objectives/exfiltration/stealer/configuration/environment"] += 1
        data["counts"] = dict(counts)
    path.write_text(json.dumps(data, indent=2) + "\n")

path = repo / "testdata/expectations.toml"
text = path.read_text()
write(path, pattern.sub(lambda m: changes[m.group()], text))
(root / "integration-repairs.json").write_text(json.dumps({"backup": str(backup), "id_changes": changes, "equivalent_selectors": receipts}, indent=2) + "\n")
print("Backup:", backup, "ID changes:", len(changes), "selector clauses:", len(receipts))
