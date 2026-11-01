# /// script
# dependencies = ["pyyaml"]
# ///
"""Verify this batch preserves effective predicates, scope and severity.

Run from any directory with uv run <this-file>.
"""
import json
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
MOVES = json.loads((HERE / "moves.json").read_text())["moves"]
RENAMES = {move["old"]: move["new"] for move in MOVES}


def normalize(rule, defaults, namespace):
    effective = {**defaults, **rule}
    for key in ("id", "desc"):
        effective.pop(key, None)

    def walk(value):
        if isinstance(value, list):
            return [walk(item) for item in value]
        if not isinstance(value, dict):
            return value
        result = {key: walk(item) for key, item in value.items()}
        if "id" in result:
            ref = result["id"]
            if "/" not in ref and "::" not in ref:
                ref = namespace + "::" + ref
            result["id"] = RENAMES.get(ref, ref)
        return result

    return walk(effective)


for move in MOVES:
    document = yaml.safe_load((ROOT / move["destination"]).read_text())
    namespace, name = move["new"].split("::")
    rule = next(rule for rule in document[move["kind"]] if rule["id"] == name)
    before = normalize(move["rule"], move["defaults"], move["old"].split("::")[0])
    after = normalize(rule, document.get("defaults", {}), namespace)
    assert before == after, move["old"]

print(f"Preserved predicates, scope and severity for {len(MOVES)} relocated rules")
