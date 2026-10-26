"""Apply the item-placement audit with scoped reference rewriting and backups.

Run once with uv run --no-project --with ruamel.yaml python <script>.
"""

import copy
import io
import json
import re
import tempfile
from collections import Counter, defaultdict
from pathlib import Path

from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap, CommentedSeq

root = Path(__file__).parent
repo = root.resolve().parents[2]
prefix = "objectives/exfiltration/stealer"
plan = json.loads((root / "item-placement-plan.json").read_text())
assert len(plan) == 1217
by_id = {r["old_id"]: r for r in plan}
yaml = YAML()
yaml.preserve_quotes = True
yaml.width = 120

documents = {}
rules = {}
original_text = {}
original_shape = {}
for rel in sorted({r["file"] for r in plan}):
    path = repo / rel
    text = path.read_text()
    doc = yaml.load(text)
    documents[rel] = doc
    original_text[rel] = text
    original_shape[rel] = copy.deepcopy(doc)
    parent = str(path.parent.relative_to(repo))
    for kind in ("traits", "composite_rules"):
        for rule in doc.get(kind, []) or []:
            full = parent + "::" + rule["id"]
            assert full in by_id, full
            rules[full] = (rel, kind, rule)
assert set(rules) == set(by_id)

# Resolve the one existing name collision by its supported source predicate.
by_id[prefix + "/cloud::swift-cloud-credential-http-exfil"]["new_name"] = "swift-mixed-store-credential-http-exfil"
by_id[prefix + "/credential::swift-cloud-credential-http-exfil"]["new_name"] = "swift-cloud-file-content-http-exfil"
id_map = {old: row["new_directory"] + "::" + row["new_name"] for old, row in by_id.items() if row["new_directory"]}
assert len(id_map.values()) == len(set(id_map.values()))
removed = set(by_id) - set(id_map)

# Matching changes are separate from item relocation and are audited below.
changes = {}


def edit(short, note, **fields):
    full = prefix + "/" + short
    rule = rules[full][2]
    rule.update(fields)
    changes[full] = note
    return rule


edit("env::kotlin-env-map-dump", "Local environment assembly is observable without implying export.", crit="notable")
edit("env::python-procfs-environ-sealed-secret-upload", "The environment read is corroboration of a proven credential uploader.", desc="Sealed credential upload accompanies a procfs environment read")
edit("env::native-forked-node-addon-form-env-http-exfil", "The non-secret install-profile alternative was removed during the source audit.", desc="Forked addon pairs secret environment names with form HTTP upload")
edit("env::github-contents-credential-fallback", "Weak name/filter-only branches were removed; a credential exporter is required.", desc="Credential export accompanies an encoded GitHub contents write")
edit("system-info/profile::js-npm-install-profile-http-get-exfil", "Co-occurrence of install context and GET does not prove that the values leave.", crit="suspicious", desc="Npm installation context appears near an HTTP GET")
edit("wallet::jvm-wallet-screenshot-http-exfil", "Robot class presence alone does not establish screenshot capture.", desc="Wallet collection and archive upload accompany a Robot API reference")
edit("multi-source::js-credential-discord-screenshot-exfiltration", "A screenshot import does not establish a second exported item.", desc="Credential export accompanies a screenshot-module import")
edit("multi-source::dotnet-chromium-surveillance-stealer", "Keyboard-hook references do not prove that input records are sent.", desc="Browser login-store targets accompany keyboard APIs and SMTP sending")
edit("ssh::python-host-profile-ssh-http-exfil", "The credential source alternative permits environment or SSH material.", desc="Host profiling accompanies an environment-or-SSH credential exporter")
edit("system-info/platform::js-concealed-platform-post", "Both item families are required.", desc="Concealed POST chains export platform and environment data")
edit("system-info/profile::ts-http-host-profile-exfil", "The source predicate requires process enumeration and environment serialization.", desc="Process and environment collection accompany HTTP export")

ssh = edit("ssh::node-ssh-env-json-http-exfil", "Require an actual environment-value copy for the second claimed item family.")
ssh["all"].append(CommentedMap(id="micro-behaviors/os/env/read::js-env-index-copy-to-object"))
setup = edit("env::pypi-setup-full-environment-oob-exfil", "Require environment data to enter an HTTP body, rather than an unrelated read and POST.")
setup["all"].append(CommentedMap(id="micro-behaviors/communications/http/request/body::python-environment-http-body-flow"))

# Separate an alternative item kind without duplicating either predicate.
profile_full = prefix + "/system-info/profile::js-system-info-exfiltration"
profile = rules[profile_full][2]
environment = copy.deepcopy(profile)
environment["id"] = "javascript-environment-json-http-export"
environment["desc"] = "Environment serialization accompanies an HTTP JSON POST"
environment["all"].append(CommentedMap(id="micro-behaviors/os/env/read::node-env-json-serialization-context"))
environment.pop("any", None)
environment["near_bytes"] = 4096
profile["any"] = CommentedSeq([CommentedMap(id="objectives/discovery/system/profile::host-process-software-locale-form")])
profile["desc"] = "Explicit host profile accompanies an HTTP JSON POST"
profile["near_bytes"] = 4096
changes[profile_full] = "The environment-only alternative becomes a configuration/environment rule; both predicates use a bounded 4096-byte context."

# Accurate triage descriptions for observations moved out of the theft tier.
descriptions = {
    "node-base64-json-data-field": "Base64 encoding appears with a JSON data field",
    "node-body-with-export-endpoint": "Request body syntax accompanies an export-like HTTP path",
    "script-http-client-send": "References an HTTP client send operation",
    "serialized-wallet-keyring-assignment": "Assigns a serialized wallet-keyring value",
    "serialized-wallet-keyring-payload-field": "Places a serialized keyring value in a payload field",
    "wallet-credential-term-cluster": "References a cluster of wallet and mnemonic terms",
    "native-export-frame-env-version": "Delimited export-frame labels name environment or version data",
    "native-export-frame-passwd-shadow": "Delimited export-frame labels name passwd or shadow data",
    "objc-account-dns-export-name-reference": "References an account-export function name",
    "export-subdomain-format": "References a formatted export subdomain",
    "master-passwd-cache-backup-path-pair": "References master.passwd and a cache backup path",
    "haxe-user-list-api-reference": "References the Haxe getUserList API name",
    "credential-or-auth-log-name": "References a credential or authentication log filename",
    "postinstall-ecs-metadata-uri-reference": "Postinstall references the ECS metadata URI variable",
    "agent-auth-json-raw-read": "Raw-read helper appears near agent authentication filenames",
    "credentials-call-json-payload-context": "Credentials-named call appears near JSON serialization",
    "js-private-key-input-request-field": "Private-key input label accompanies a JSON request field",
    "node-file-bucket-json-fields": "References environment, JSON and document bucket fields",
    "node-obfuscated-export-awaiter-invocation": "Invokes an obfuscated export/awaiter call shape",
    "go-stealer-feature-switch-struct": "Go type descriptors name a set of stealer feature switches",
    "managed-discord-token-scan-routines-reference": "References Discord token-scanning routine names",
    "managed-telegram-session-capture-routines-reference": "References Telegram session-capture routine names",
    "page-content-payload-field": "References a DOM or HTML payload field",
    "screenshot-payload-field": "References a screenshot payload field",
    "swift-ssh-key-report-label": "References an SSH_KEY report label",
    "rust-process-json-payload-reference": "References process-report type and field names",
    "managed-infection-type-report-field": "Managed metadata contains an infection-type report field",
    "cursor-auth-bridge-log-message": "References a Cursor authentication bridge log message",
    "documents-downloads-search-root-pair": "References Documents and Downloads search roots",
    "zig-resolver-credential-path-proximity": "Resolver source text appears near credential-file paths",
    "zig-hex-label-format-reference": "References a hexadecimal alphabet and formatted labels",
    "declared-stealer-upload-header": "Declares a stealer-upload HTTP header",
    "node-sensitive-config-read-proximity": "Directory enumeration and reads appear near sensitive filenames",
    "npm-postinstall-cloud-container-secret-stage": "Npm postinstall stages cloud and container secret files",
}
for old, row in by_id.items():
    if row["new_directory"] and not row["new_directory"].startswith(prefix):
        rule = rules[old][2]
        if row["new_directory"].startswith(("micro-behaviors/", "metadata/")):
            rule["crit"] = "notable"
            rule.pop("attack", None)
            rule.pop("mbc", None)
        if row["new_name"] in descriptions:
            rule["desc"] = descriptions[row["new_name"]]
        elif "url/path" in row["new_directory"]:
            rule["desc"] = "References " + row["new_name"].replace("-", " ")
        elif old.startswith(prefix + "/surveillance::"):
            rule["desc"] = rule["desc"].replace("surveillance vocabulary fragment", "spyware vocabulary reference")
        changes.setdefault(old, "The observation is retained in its supported non-export home; neutral observations are notable.")

# Old directory selectors are expanded to their surviving export members.
# This preserves their observed member set across the new item homes and drops
# helpers that no longer make an export claim.
old_directories = defaultdict(list)
for old, row in by_id.items():
    if row["new_directory"] and row["new_directory"].startswith(prefix):
        old_directories[old.split("::")[0]].append(id_map[old])
selector_changes = []


def references(value, old_parent, new_parent, context="", file=""):
    if isinstance(value, dict):
        for key, child in list(value.items()):
            if key == "id" and isinstance(child, str):
                full = child if "/" in child or "::" in child else old_parent + "::" + child
                if full in removed:
                    raise AssertionError(("reference to removed unsupported claim", file, full))
                if full in id_map:
                    new = id_map[full]
                    value[key] = new.split("::")[1] if "/" not in child and "::" not in child and new.split("::")[0] == new_parent else new
            elif key != "id":
                references(child, old_parent, new_parent, key, file)
    elif isinstance(value, list):
        expanded = []
        for child in value:
            if isinstance(child, dict) and isinstance(child.get("id"), str):
                selector = child["id"].rstrip("/")
                if selector in old_directories and selector != prefix:
                    assert context in ("any", "unless"), (file, context, selector)
                    members = sorted(set(old_directories[selector]))
                    expanded.extend(CommentedMap(id=name) for name in members)
                    selector_changes.append({"file": file, "condition": context, "old_selector": child["id"], "new_members": members})
                    continue
            references(child, old_parent, new_parent, context, file)
            expanded.append(child)
        value[:] = expanded


for old, (rel, _, rule) in rules.items():
    if old in removed:
        continue
    new_parent = by_id[old]["new_directory"]
    for key, val in list(rule.items()):
        if key != "id":
            references(val, old.split("::")[0], new_parent, key, rel)
    rule["id"] = id_map[old].split("::")[1]
references(environment, profile_full.split("::")[0], prefix + "/configuration/environment", file=rules[profile_full][0])

new_files = {}
new_rules = []
for rel, doc in documents.items():
    groups = defaultdict(lambda: {"traits": [], "composite_rules": []})
    for old, (source, kind, rule) in rules.items():
        if source == rel and old not in removed:
            groups[by_id[old]["new_directory"]][kind].append(rule)
    if rel == rules[profile_full][0]:
        groups[prefix + "/configuration/environment"]["composite_rules"].append(environment)
    for target, kinds in groups.items():
        new_doc = copy.deepcopy(doc)
        for kind in ("traits", "composite_rules"):
            if kinds[kind]:
                new_doc[kind] = CommentedSeq(kinds[kind])
            else:
                new_doc.pop(kind, None)
        if target.startswith(("micro-behaviors/", "metadata/")):
            defaults = new_doc.get("defaults", {})
            defaults.pop("attack", None)
            defaults.pop("mbc", None)
        name = Path(rel).name
        destination = target + "/" + name
        if destination in new_files or (not target.startswith(prefix) and (repo / destination).exists()):
            stem = str(Path(rel).parent).split("stealer/")[-1].replace("/", "-")
            destination = target + "/stealer-" + stem + "-" + name
        assert destination not in new_files, destination
        assert not (repo / destination).exists() or destination in original_text, ("would overwrite an unrelated file", destination)
        if len(groups) == 1 and new_doc == original_shape[rel]:
            text = original_text[rel]
        else:
            stream = io.StringIO()
            yaml.dump(new_doc, stream)
            text = stream.getvalue()
        new_files[destination] = text
        new_rules.extend((target, r["id"]) for kind in ("traits", "composite_rules") for r in new_doc.get(kind, []))

assert len(new_rules) == len(set(new_rules))
assert len(new_rules) == len(plan) - len(removed) + 1

# Use simultaneous replacement so a new ID that equals another old ID cannot
# be rewritten a second time. A trailing ID boundary avoids prefix changes.
changed_ids = {old: new for old, new in id_map.items() if old != new}
pattern = re.compile("(?:" + "|".join(re.escape(k) for k in sorted(changed_ids, key=len, reverse=True)) + r")(?![A-Za-z0-9_-])")


def substitute(text):
    return pattern.sub(lambda m: changed_ids[m.group()], text)


# Rules within new_files already have their references resolved above.
# External rule consumers need full-ID rewriting plus selector expansion.
external = {}
for tier in ("micro-behaviors", "objectives", "metadata", "well-known"):
    for path in (repo / tier).rglob("*.yaml"):
        rel = str(path.relative_to(repo))
        if rel in original_text:
            continue
        text = path.read_text()
        needs_selector = any(re.search(r"id:\s*[\"']?" + re.escape(old) + r"/?[\"']?\s*(?:#.*)?$", text, re.M) for old in old_directories)
        after = substitute(text)
        if needs_selector:
            doc = yaml.load(after)
            for kind in ("traits", "composite_rules"):
                for rule in doc.get(kind, []) or []:
                    for key, value in list(rule.items()):
                        if key != "id":
                            references(value, str(path.parent.relative_to(repo)), str(path.parent.relative_to(repo)), key, rel)
            stream = io.StringIO()
            yaml.dump(doc, stream)
            after = stream.getvalue()
        if after != text:
            external[rel] = (text, after)

expectations = "testdata/expectations.toml"
text = (repo / expectations).read_text()
if substitute(text) != text:
    external[expectations] = (text, substitute(text))

# Verify current input bytes and retain a complete recovery copy before writes.
backup = Path(tempfile.mkdtemp(prefix="stealer-items-backup-"))
for rel, text in original_text.items():
    assert (repo / rel).read_text() == text
    dest = backup / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(text)
for rel, (before, _) in external.items():
    assert (repo / rel).read_text() == before
    dest = backup / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(before)
for rel, text in new_files.items():
    path = repo / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
for rel in set(original_text) - set(new_files):
    (repo / rel).unlink()
for rel, (_, after) in external.items():
    (repo / rel).write_text(after)

audit = []
for row in plan:
    old = row["old_id"]
    audit.append({"old_id": old, "new_id": id_map.get(old), "action": "remove-unsupported-claim" if old in removed else "move" if old != id_map[old] else "retain", "reason": row["reason"], "predicate_or_level_change": changes.get(old), "required_refs_before": row["required_refs"]})
(root / "item-placement-audit.json").write_text(json.dumps({"reviewed": len(plan), "surviving_rules": len(new_rules), "backup": str(backup), "counts": dict(Counter(target for target, _ in new_rules)), "rules": audit}, indent=2) + "\n")
(root / "item-id-map.json").write_text(json.dumps(id_map, indent=2) + "\n")
(root / "selector-migration.json").write_text(json.dumps(selector_changes, indent=2) + "\n")
print("backup", backup)
print("reviewed", len(plan), "removed unsupported", len(removed), "result", len(new_rules))
for target, count in sorted(Counter(target for target, _ in new_rules).items()):
    if count > 100:
        print("REVIEWED BUDGET REQUIRED", count, target)
