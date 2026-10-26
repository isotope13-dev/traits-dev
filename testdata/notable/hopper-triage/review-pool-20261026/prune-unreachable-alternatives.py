"""Drop migrated explicit alternatives that cannot match a Python caller."""
raise SystemExit("Historical attempt reverted: file scopes can correlate decoded payload layers. Do not rerun.")

import io
import json
from pathlib import Path

import yaml as fast
from ruamel.yaml import YAML

root = Path(__file__).parent
repo = root.resolve().parents[2]
definitions = {}
for tier in ("micro-behaviors", "objectives", "metadata", "well-known"):
    for path in (repo / tier).rglob("*.yaml"):
        doc = fast.load(path.read_text(), Loader=fast.CSafeLoader) or {}
        for kind in ("traits", "composite_rules"):
            for rule in doc.get(kind, []) or []:
                full = rule["id"] if "::" in rule["id"] else str(path.parent.relative_to(repo)) + "::" + rule["id"]
                definitions[full] = {**(doc.get("defaults") or {}), **rule}

def python_possible(rule):
    if rule.get("if", {}).get("type") in ("path", "basename", "dirname"):
        return True
    entries = rule.get("for")
    if not entries:
        return True
    parts = {part.strip().lower() for entry in entries for part in entry.split(",")}
    # Source and binary groups do not include Python source. The caller's
    # concrete Python origin cannot satisfy any of those alternatives.
    return bool(parts & {"python", "scripts", "all", "*"}) and not bool(parts & {"!python", "-python"})

yaml = YAML()
yaml.preserve_quotes = True
yaml.width = 120
receipts = []
for rel in (
    "objectives/credential-access/theft/multi-store/python-source-marker.yaml",
    "objectives/exfiltration/http/collect/python-infostealer.yaml",
):
    path = repo / rel
    doc = yaml.load(path.read_text())
    rule = doc["composite_rules"][0]
    assert rule.get("for", doc["defaults"].get("for")) == ["python"]
    removed = []
    kept = []
    for leg in rule["any"]:
        ref = leg.get("id")
        if ref in definitions and not python_possible(definitions[ref]):
            removed.append({"id": ref, "declared_types": definitions[ref].get("for")})
        else:
            kept.append(leg)
    rule["any"] = kept
    stream = io.StringIO()
    yaml.dump(doc, stream)
    path.write_text(stream.getvalue().rstrip() + "\n")
    receipts.append({"rule": str(path.parent.relative_to(repo)) + "::" + rule["id"], "removed_unreachable_alternatives": removed, "remaining_alternatives": len(kept)})
    print(rule["id"], "removed", len(removed), "kept", len(kept))
(root / "unreachable-alternatives.json").write_text(json.dumps(receipts, indent=2) + "\n")
