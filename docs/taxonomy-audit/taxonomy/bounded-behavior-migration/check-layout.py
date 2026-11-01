# /// script
# dependencies = ["pyyaml"]
# ///
"""Check destination headroom and retired namespaces; print calculated counts."""
from collections import Counter
import json
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
MOVES = json.loads((HERE / "moves.json").read_text())["moves"]
DESTINATIONS = {str(Path(move["destination"]).parent) for move in MOVES}
physical = Counter()
namespaces = Counter()
for branch in ("metadata", "micro-behaviors", "objectives", "well-known"):
    for path in (ROOT / branch).rglob("*.yaml"):
        document = yaml.load(path.read_text(), Loader=yaml.CSafeLoader) or {}
        parent = str(path.parent.relative_to(ROOT))
        for kind in ("traits", "composite_rules"):
            for rule in document.get(kind, []) or []:
                physical[parent] += 1
                name = rule["id"]
                namespace = name.split("::")[0] if "::" in name else parent
                namespaces[namespace] += 1

errors = []
counts = {}
for directory in sorted(DESTINATIONS):
    counts[directory] = {
        "physical": physical[directory],
        "namespace": namespaces[directory],
    }
    for population, count in counts[directory].items():
        if count >= 72:
            errors.append(f"{directory}: {population}={count}; split at 72, before the 80-rule cap")

for retired in (
    "micro-behaviors/data/db/sql",
    "micro-behaviors/process/create/spawn",
    "objectives/exfiltration/serialization",
):
    count = sum(value for name, value in namespaces.items()
                if name == retired or name.startswith(retired + "/"))
    if count:
        errors.append(f"{retired}: {count} rules remain")

print(json.dumps(counts, indent=2))
if errors:
    raise SystemExit("\n".join(errors))
