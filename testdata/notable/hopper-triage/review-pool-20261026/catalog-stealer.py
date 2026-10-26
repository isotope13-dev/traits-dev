"""Catalog stealer rules and trace required environment observations.

Run with uv run --no-project --with pyyaml python <script>.
Exclusions and downgrades are deliberately excluded from source tracing.
"""

import json
import re
from pathlib import Path

import yaml


repo = Path(__file__).resolve().parents[3]
output = Path(__file__).parent
catalog = {}
for tier in ("micro-behaviors", "objectives", "metadata", "well-known"):
    for path in sorted((repo / tier).rglob("*.yaml")):
        data = yaml.load(path.read_text(), Loader=yaml.CSafeLoader) or {}
        if not isinstance(data, dict):
            continue
        for kind in ("traits", "composite_rules"):
            for rule in data.get(kind, []) or []:
                if not isinstance(rule, dict) or "id" not in rule:
                    continue
                name = rule["id"]
                parent = str(path.parent.relative_to(repo))
                full = name if "::" in name else f"{parent}::{name}"
                catalog[full] = {
                    "id": full,
                    "file": str(path.relative_to(repo)),
                    "defaults": data.get("defaults", {}),
                    "kind": kind,
                    "rule": rule,
                }


def required_refs(value, parent):
    refs = []
    if isinstance(value, dict):
        if "id" in value and isinstance(value["id"], str):
            name = value["id"]
            refs.append(name if "/" in name or "::" in name else f"{parent}::{name}")
        for key, item in value.items():
            if key not in ("unless", "downgrade", "id"):
                refs.extend(required_refs(item, parent))
    elif isinstance(value, list):
        for item in value:
            refs.extend(required_refs(item, parent))
    return refs


for full, item in catalog.items():
    parent = full.split("::")[0]
    rule = item["rule"]
    item["required_refs"] = sorted(set(required_refs({k: rule[k] for k in ("if", "all", "any") if k in rule}, parent)))


def trace_env(full, seen=None, depth=0):
    if seen is None:
        seen = set()
    if full in seen or depth > 8:
        return set()
    seen.add(full)
    found = set()
    item = catalog.get(full)
    if item is None:
        return found
    for ref in item["required_refs"]:
        if ref.startswith(("micro-behaviors/os/env/", "objectives/credential-access/env/")):
            found.add(ref)
        if ref in catalog:
            found.update(trace_env(ref, seen, depth + 1))
    return found


stealers = []
for full, item in sorted(catalog.items()):
    if not full.startswith("objectives/exfiltration/stealer/"):
        continue
    item = dict(item)
    item["environment_evidence"] = sorted(trace_env(full))
    content = {k: item["rule"][k] for k in ("id", "desc", "if", "all", "any") if k in item["rule"]}
    item["environment_text"] = bool(re.search(r"(?:\benv\b|environ|getenv|dotenv|ci[-_ ](?:token|secret))", json.dumps(content), re.I))
    stealers.append(item)

(output / "stealer-catalog.json").write_text(json.dumps(stealers, indent=2) + "\n")
candidates = [r for r in stealers if (r["environment_evidence"] or r["environment_text"]) and not r["id"].startswith("objectives/exfiltration/stealer/env::")]
(output / "stealer-env-candidates.json").write_text(json.dumps(candidates, indent=2) + "\n")
print(f"{len(catalog)} total rules; {len(stealers)} stealer rules; {len(candidates)} environment candidates outside env")
for item in candidates:
    print(item["id"], "|", item["rule"].get("desc", ""), "|", ", ".join(item["environment_evidence"][:4]))
