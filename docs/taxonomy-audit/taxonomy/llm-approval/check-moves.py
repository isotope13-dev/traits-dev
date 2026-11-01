# /// script
# dependencies = ["pyyaml"]
# ///
"""Verify approval-rule moves, effective defaults and capacity."""
from collections import Counter
import json
from pathlib import Path
import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
manifest = json.loads((HERE / "moves.json").read_text())
moves = manifest["moves"]
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
    if name == "agent-persona-and-gate-takeover":
        # The rebased branch removed this rule and its supporting traits.
        assert all(r["id"] != name for r in doc[move["kind"]])
        continue
    rule = next(r for r in doc[move["kind"]] if r["id"] == name)
    before = {**move["defaults"], **move["before"]}
    after = {**(doc.get("defaults") or {}), **rule}
    before.pop("id")
    after.pop("id")
    if name == "agent-config-approval-bypass-clues":
        # Preserve the other branch's narrower approval indicators.
        retired = {
            "micro-behaviors/data/llm/permission::agent-permission-wildcard-allow",
            "micro-behaviors/data/llm/permission::agent-permission-allow-assignment",
        }
        before["any"] = [item for item in before["any"] if item["id"] not in retired]
    assert normalize(before, move["old"].split("::")[0]) == normalize(after, namespace), move["old"]

exceptions = yaml.safe_load((ROOT / "objectives/evasion/security-bypass/llm/override/agent-config-hijack.yaml").read_text())
by_id = {rule["id"]: rule for rule in exceptions["composite_rules"]}
assert exceptions.get("defaults") == manifest["retained_exceptions"]["defaults"]
for original in manifest["retained_exceptions"]["rules"]:
    assert by_id[original["id"]] == original, original["id"]
assert set(by_id) == {"headless-agent-runner-isolated-session", "agent-config-user-initiated-context", "harness-provisioned-child-agent-config"}
assert all(rule["crit"] == "exception" for rule in by_id.values())
assert [item["id"] for item in by_id["agent-config-user-initiated-context"]["any"]] == [
    "headless-agent-runner-isolated-session",
    "micro-behaviors/data/llm/permission::allow-everywhere-approval-reply",
    "harness-provisioned-child-agent-config",
]
assert [item["id"] for item in by_id["headless-agent-runner-isolated-session"]["all"]] == [
    "micro-behaviors/data/llm/session::agent-isolated-session-launch",
    "micro-behaviors/data/llm/permission::ai-agent-bypass-permissions-mode",
]
assert [item["id"] for item in by_id["harness-provisioned-child-agent-config"]["all"]] == [
    "micro-behaviors/os/env/runtime::opencode-config-env-isolated-session",
    "metadata/lang/source/literal/array::egress-command-array-head",
]

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
for directory in ("objectives/evasion/security-bypass/llm/override", "objectives/evasion/security-bypass/llm/approval"):
    print(f"{directory}: {physical[directory]} physical, {namespaces[directory]} namespace")
    assert physical[directory] < 72 and namespaces[directory] < 72, directory
print(f"Verified predicates, scope and severity of {len(moves) - 1} moves and one retired rule")
