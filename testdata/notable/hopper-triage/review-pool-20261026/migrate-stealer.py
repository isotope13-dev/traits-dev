"""Superseded draft of source-boundary corrections; do not apply.

Run once with: uv run --no-project --with ruamel.yaml python <script>
The placement audit records every reviewed stealer rule and each move's reason.
"""

raise SystemExit("Source-first migration suspended while the item-first taxonomy is reviewed.")

import copy
import json
from collections import Counter, defaultdict
from pathlib import Path

from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap, CommentedSeq


repo = Path(__file__).resolve().parents[3]
output = Path(__file__).parent
prefix = "objectives/exfiltration/stealer/"
yaml = YAML()
yaml.preserve_quotes = True
yaml.width = 120
yaml.indent(mapping=2, sequence=4, offset=2)

# Each tuple names the supported source or neutral observation, not a backend.
moves = {}


def move(old, target, reason, name=None):
    moves[prefix + old] = (target if target.startswith(("objectives/", "micro-behaviors/")) else prefix + target, name, reason)


for name in ("ci-secret-file-to-request-collector", "gha-encoded-environment-log", "ci-secret-bound-curl-file-upload", "ci-token-curl-upload", "dotenv-full-environment-http-exfil"):
    move("env::" + name, "dev-secret", "Required workflow secret or dotenv source is a developer-secret store.")
move("env::python-procfs-environ-sealed-secret-upload", "dev-secret", "The proven upload source is the referenced developer-secret bundle; a nearby procfs read does not prove that environment bytes leave.", "python-sealed-dev-secret-upload-with-procfs-read")
move("env::elixir-onload-env-file-http-exfil", "multi-source", "Environment selection and a developer credential-file source are both required.")
move("env::npm-runtime-host-profile-credential-exfil", "multi-source", "Local network identity and credential-bearing environment configuration are both required.")
move("env::npm-install-profile-near-raw-ip-http-get", "system-info/profile", "Required source is npm installation metadata and hostname, with no secret export proven.")
move("env::install-hook-fingerprint-identity-exfil", "system-info/identity", "Hashed device identity and Git identity are host identifiers, not a process-environment export.")
move("env::native-forked-node-addon-form-profile-exfil", "system-info/identity", "Required hostname and user queries identify the host/user source; getenv alone does not establish environment export.")
move("env::kotlin-env-map-dump", "micro-behaviors/os/env/dump", "Environment assembly has no required send and is a neutral capability.")
move("env::node-base64-json-exfil-body", "micro-behaviors/data/encode/base64", "Required evidence is Base64 encoding and a JSON data field, with no source or network sink.", "node-base64-json-data-field")

move("account-db::native-credential-tcp-exfil", "multi-source", "Shadow account data and process-environment data are independently required.")
move("cloud::go-cloud-env-credential-exfil", "credential", "Alternative required sources are cloud files or process environments; the common source is credential material.", "go-mixed-store-credential-exfil")
move("cloud::go-binary-cloud-env-credential-exfil", "credential", "Alternative required sources are cloud files or process environments; the common source is credential material.", "go-binary-mixed-store-credential-exfil")
move("cloud::swift-cloud-credential-http-exfil", "credential", "Two-of-three source alternatives can include process environment or cloud stores; cloud is not required by every passing combination.", "swift-mixed-store-credential-http-exfil")
move("cloud::swift-cloud-message-http-exfil", "credential", "The required parent permits environment or cloud credential stores.", "swift-mixed-store-message-http-exfil")
move("credential::swift-cloud-credential-http-exfil", "cloud", "A cloud credential-file source is required in every match.", "swift-cloud-file-content-http-exfil")
move("cloud::swift-host-profile-http-exfil", "multi-source", "A credential export and independent host identity/platform profile are both required.")
move("cloud::swift-imds-env-secret-post", "multi-source", "Both process-environment secrets and cloud IMDS acquisition are required.")
move("cloud::npm-postinstall-ecs-container-metadata-url", "micro-behaviors/os/env/cloud", "The matcher only references an ECS metadata environment variable in postinstall.", "postinstall-ecs-container-metadata-uri-reference")
move("credential::js-private-key-env-http-exfiltration", "env", "The immediate secret store is the process environment; key format does not change the store.")
move("credential::developer-token-discord-webhook-export", "env", "The bound Axios body source is an environment token, with repository context as corroboration.", "developer-token-chat-export-with-repository-context")
move("dev-secret::cicd-environ-trycloudflare-exfil", "env", "Procfs process environments are the required source; no workflow secret expression or developer credential file is required.")
move("dev-secret::node-ci-token-tunnel-post-cooccurrence", "env", "The required token source is process.env, rather than a workflow secret store.")
move("dev-secret::shopify-token-host-diversion", "env", "The source leg is a credential-bearing environment variable.")
move("dev-secret::shell-developer-secret-stealer", "credential", "Alternatives admit environment secrets or credential files, so no single developer-file store is required.")
move("dev-secret::postinstall-dev-secret-oob-exfil", "multi-source", "Developer credential-file access and init-process environment targeting are both required.")
move("dev-secret::node-developer-credential-sweep", "credential", "The required path set spans credential stores beyond developer configuration.")
move("dev-secret::node-developer-secret-multipart-exfil-archive", "credential", "The required source cluster permits wallet or developer credentials; their common class is credential material.")
move("dev-secret::node-dev-secrets-clipboard-history-exfil", "credential", "The proven export is credential-associated file upload; adjacent clipboard/history use does not bind a second exported source.")
move("dev-secret::node-financial-account-http-exfil", "credential", "Financial account authentication material is required; developer credential configuration is not.")
move("dev-secret::node-dev-secret-source-cluster", "objectives/credential-access/theft/multi-app", "Source references and collection output markers have no required send.", "node-credential-source-cluster")
move("dev-secret::npm-postinstall-cloud-secret-file-stage", "objectives/credential-access/cloud/container", "The matcher establishes local cloud/container secret staging and has no send leg.", "npm-postinstall-cloud-container-secret-stage")
move("dev-secret::rust-project-env-exfil-endpoint", "micro-behaviors/communications/http/url/path", "A literal API route is a path reference and establishes no theft.", "rust-project-env-api-path")
move("dev-secret::node-custom-exfil-sink", "micro-behaviors/communications/http/request/body", "The matcher combines an export-like endpoint with request-body syntax, without a sensitive source.", "node-body-with-export-endpoint")
move("multi-source::go-windows-collect-credential-exfil", "credential", "The any branch requires only one credential source; multiple independent sources are not required.")
move("multi-source::shell-ai-provider-key-harvest-upload", "env", "All source observations refer to provider keys from the same process-environment store.")
move("ssh::node-ssh-env-json-http-exfil", "multi-source", "The corrected matcher requires SSH file acquisition and an environment-value copy.")
move("ssh::python-host-profile-ssh-http-exfil", "multi-source", "A host profile is required alongside a credential exporter whose source can be environment or SSH.", "python-host-profile-credential-http-exfil")
move("system-info/identity::python-host-identity-with-environment-export", "multi-source", "Both a complete environment exporter and a host-identity send are required.")
move("system-info/platform::js-concealed-platform-post", "multi-source", "Both OS platform export and full environment export are required.", "js-concealed-platform-env-post")
move("system-info/profile::shell-macos-host-http-exfil", "multi-source", "Environment dump, listener inventory and CPU/OS profile are independently required.")
move("system-info/profile::ts-http-host-profile-exfil", "multi-source", "The source predicate requires process enumeration together with environment serialization.", "ts-process-env-http-exfil")
for name in ("js-wallet-private-key-env-sent-in-header", "python-wallet-env-key-urllib-json-exfil", "rust-wallet-private-key-curl-exfiltration"):
    move("wallet::" + name, "env", "The key is acquired from a process-environment variable; no wallet store is required.")

removed = {
    prefix + "dev-secret::apify-actor-data-theft": "Actor method wrapping, platform identity variables and fetch do not establish a sensitive source-to-send path.",
    prefix + "dev-secret::node-developer-credential-stealer": "The clipboard alternative has no required export; collection and export are already represented by their specific rules.",
    prefix + "dev-secret::npm-install-hook-workflow-token-contents-write": "Using an environment token to authenticate a repository write does not establish token exfiltration.",
    prefix + "system-info/profile::native-netscaler-system-http-exfil": "An environ or procfs reference next to a beacon does not establish a host-report export.",
}

docs = {}
original = {}
for path in sorted((repo / prefix).rglob("*.yaml")):
    doc = yaml.load(path.read_text())
    if not isinstance(doc, dict):
        continue
    docs[path] = doc
    parent = str(path.parent.relative_to(repo))
    for kind in ("traits", "composite_rules"):
        for rule in doc.get(kind, []) or []:
            full = rule["id"] if "::" in rule["id"] else parent + "::" + rule["id"]
            original[full] = (path, kind, rule)

assert set(moves) <= set(original), sorted(set(moves) - set(original))
assert set(removed) <= set(original), sorted(set(removed) - set(original))
assert len(original) == 1217
id_map = {old: target + "::" + (name or old.split("::")[1]) for old, (target, name, _) in moves.items()}

# Predicate corrections from the review. Placement and matching changes are
# recorded separately in the generated audit.
original[prefix + "env::kotlin-env-map-dump"][2]["crit"] = "notable"
original[prefix + "env::python-procfs-environ-sealed-secret-upload"][2]["desc"] = "Sealed developer-secret upload accompanies a procfs environment read"
original[prefix + "env::native-forked-node-addon-form-env-http-exfil"][2]["desc"] = "Forked Node addon pairs secret environment names with form HTTP upload"
original[prefix + "env::env-vars"][2]["id"] = "encoded-env-secret-http-exfil"
id_map[prefix + "env::env-vars"] = prefix + "env::encoded-env-secret-http-exfil"
for old, new_desc in {
    "cloud::go-cloud-env-credential-exfil": "Go exports credentials from a cloud-file or environment source",
    "cloud::go-binary-cloud-env-credential-exfil": "Go binary exports credentials from a cloud-file or environment source",
    "cloud::swift-cloud-credential-http-exfil": "Swift sends credentials selected from mixed secret stores over HTTP",
    "cloud::swift-cloud-message-http-exfil": "Swift mixed-store credential export with a message endpoint",
    "ssh::python-host-profile-ssh-http-exfil": "Host profile accompanies an environment-or-SSH credential exporter",
    "system-info/platform::js-concealed-platform-post": "Concealed POST chains export OS platform and process environment",
    "system-info/profile::ts-http-host-profile-exfil": "Process enumeration and environment serialization accompany HTTP export",
    "dev-secret::node-dev-secret-source-cluster": "Credential source references or collection output markers",
    "dev-secret::node-dev-secrets-clipboard-history-exfil": "Credential-associated file upload near clipboard or history activity",
    "dev-secret::node-custom-exfil-sink": "Request body syntax near an export-like HTTP endpoint",
    "dev-secret::rust-project-env-exfil-endpoint": "Project environment API path reference",
    "cloud::npm-postinstall-ecs-container-metadata-url": "Postinstall references the ECS metadata URI environment variable",
}.items():
    original[prefix + old][2]["desc"] = new_desc
for old in ("dev-secret::node-custom-exfil-sink", "dev-secret::rust-project-env-exfil-endpoint", "cloud::npm-postinstall-ecs-container-metadata-url"):
    original[prefix + old][2]["crit"] = "notable"

ssh_rule = original[prefix + "ssh::node-ssh-env-json-http-exfil"][2]
ssh_rule["all"].append(CommentedMap(id="micro-behaviors/os/env/read::js-env-index-copy-to-object"))

# Split a genuine source alternative rather than filing environment export
# under host-profile. Preserve the host-profile predicate in the original.
profile_id = prefix + "system-info/profile::js-system-info-exfiltration"
profile_path, profile_kind, profile_rule = original[profile_id]
env_rule = copy.deepcopy(profile_rule)
env_rule["id"] = "javascript-environment-json-http-export"
env_rule["desc"] = "Environment JSON serialization accompanies an HTTP JSON POST"
env_rule["all"].append(CommentedMap(id="micro-behaviors/os/env/read::node-env-json-serialization-context"))
env_rule.pop("any", None)
env_rule["near_bytes"] = 4096
profile_rule["any"] = CommentedSeq([CommentedMap(id="objectives/discovery/system/profile::host-process-software-locale-form")])
profile_rule["desc"] = "Explicit host profile accompanies an HTTP JSON POST"
profile_rule["near_bytes"] = 4096


def rewrite_refs(value, old_parent, definition=False):
    if isinstance(value, dict):
        for key, child in list(value.items()):
            if key == "id" and isinstance(child, str) and not definition:
                full = child if "/" in child or "::" in child else old_parent + "::" + child
                if full in removed:
                    raise AssertionError(("reference to removed rule", full))
                if full in id_map:
                    value[key] = id_map[full]
                elif full in original and "/" not in child and "::" not in child:
                    value[key] = full
            elif key != "id":
                rewrite_refs(child, old_parent)
    elif isinstance(value, list):
        for child in value:
            rewrite_refs(child, old_parent)


for full, (_, _, rule) in original.items():
    if full not in removed:
        rewrite_refs(rule, full.split("::")[0], definition=True)
rewrite_refs(env_rule, profile_id.split("::")[0], definition=True)

audit = []
for old, (path, kind, rule) in original.items():
    if old in removed:
        action, reason, new = "remove-unsupported-claim", removed[old], None
    elif old in moves:
        action, reason, new = "move", moves[old][2], id_map[old]
    else:
        action, reason, new = "retain", "Required source remains compatible with its current store; environment references used only for paths, authentication, identity or corroboration do not change that source.", id_map.get(old, old)
    audit.append({"old_id": old, "new_id": new, "action": action, "reason": reason, "original_file": str(path.relative_to(repo))})

for path, doc in docs.items():
    old_parent = str(path.parent.relative_to(repo))
    groups = defaultdict(lambda: {"traits": [], "composite_rules": []})
    for full, (source, kind, rule) in original.items():
        if source != path or full in removed:
            continue
        target = moves.get(full, (old_parent, None, None))[0]
        new_id = id_map.get(full, full)
        rule["id"] = new_id.split("::")[1]
        groups[target][kind].append(rule)
    if path == profile_path:
        groups[prefix + "env"][profile_kind].append(env_rule)
    if not groups:
        path.unlink()
        continue
    for target, rules in groups.items():
        new_doc = copy.deepcopy(doc)
        for kind in ("traits", "composite_rules"):
            if rules[kind]:
                new_doc[kind] = CommentedSeq(rules[kind])
            else:
                new_doc.pop(kind, None)
        if target.startswith("micro-behaviors/"):
            defaults = new_doc.get("defaults", {})
            defaults.pop("attack", None)
            defaults.pop("mbc", None)
            defaults["crit"] = "notable"
            for kind in ("traits", "composite_rules"):
                for rule in new_doc.get(kind, []):
                    rule.pop("attack", None)
                    rule.pop("mbc", None)
        destination = repo / target / path.name
        if target != old_parent and destination.exists():
            destination = destination.with_name(path.parent.name + "-" + path.name)
            assert not destination.exists(), destination
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("w") as handle:
            yaml.dump(new_doc, handle)
    if old_parent not in groups:
        path.unlink()

# External references carry full IDs. Update rule and expectation consumers;
# historical scan JSON remains an immutable record of the earlier engine.
for tier in ("micro-behaviors", "objectives", "metadata", "well-known"):
    for path in (repo / tier).rglob("*.yaml"):
        before = path.read_text()
        after = before
        for old, new in id_map.items():
            after = after.replace(old, new)
        if after != before:
            path.write_text(after)
expectations = repo / "testdata/expectations.toml"
before = expectations.read_text()
after = before
for old, new in id_map.items():
    after = after.replace(old, new)
if after != before:
    expectations.write_text(after)

(output / "stealer-placement-audit.json").write_text(json.dumps({"reviewed": len(audit), "actions": dict(Counter(r["action"] for r in audit)), "rules": audit}, indent=2) + "\n")
(output / "stealer-id-map.json").write_text(json.dumps(id_map, indent=2) + "\n")
print(Counter(r["action"] for r in audit))
