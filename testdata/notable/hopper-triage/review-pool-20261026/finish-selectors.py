"""Limit selector edits to consumers of the migrated stolen-item classes."""
import io
import json
from pathlib import Path

from ruamel.yaml import YAML

root = Path(__file__).parent
repo = root.resolve().parents[2]
receipt = json.loads((root / "integration-repairs.json").read_text())
backup = Path(receipt["backup"])
yaml = YAML()
yaml.preserve_quotes = True
yaml.width = 120
clauses = receipt["equivalent_selectors"]
files = {}
for row in clauses:
    directory, name = row["rule"].split("::", 1)
    for path in (repo / directory).glob("*.yaml"):
        # Searching a few directory siblings is much cheaper than parsing the tree.
        if row["rule"] in files:
            break
        if name.split("::")[-1] in path.read_text():
            doc = yaml.load(path.read_text()) or {}
            for rule in doc.get("composite_rules", []) or []:
                if rule["id"] == name or directory + "::" + rule["id"] == row["rule"]:
                    files[row["rule"]] = path
                    break
    assert row["rule"] in files, row["rule"]

for path in set(files.values()):
    original = backup / path.relative_to(repo)
    assert original.exists(), path
    path.write_text(original.read_text())

retained = []
for row in clauses:
    if row["clause"] != "any" or len(row["before"]) == len(row["after"]):
        continue
    if not any("objectives/exfiltration/stealer" in str(leg) for leg in row["before"]):
        continue
    path = files[row["rule"]]
    doc = yaml.load(path.read_text())
    rule = next(r for r in doc["composite_rules"] if row["rule"].endswith("::" + r["id"]))
    rule["any"] = row["after"]
    stream = io.StringIO()
    yaml.dump(doc, stream)
    path.write_text(stream.getvalue().rstrip() + "\n")
    retained.append(row)

# These two source/staging helpers are component/notable observations. Their
# observations remain true when a more specific theft verdict also matches.
# Do not recreate the retired store taxonomy solely to suppress that overlap.
suppression_changes = []
for rel in (
    "objectives/command-and-control/dropper/staged-loader/python-stealer-marker.yaml",
    "objectives/credential-access/theft/multi-store/python-source-marker.yaml",
):
    path = repo / rel
    doc = yaml.load(path.read_text())
    rule = doc["composite_rules"][0]
    before = list(rule.get("unless", []))
    after = [leg for leg in before if not leg.get("id", "").startswith("objectives/exfiltration/stealer/")]
    if after:
        rule["unless"] = after
    else:
        rule.pop("unless", None)
    stream = io.StringIO()
    yaml.dump(doc, stream)
    path.write_text(stream.getvalue().rstrip() + "\n")
    suppression_changes.append({"rule": str(path.parent.relative_to(repo)) + "::" + rule["id"], "level": rule["crit"], "before": before, "after": after, "rationale": "A component/notable source or staging observation remains valid when a more specific theft verdict also matches. No hostile or suspicious rule is relaxed."})

receipt["equivalent_selectors"] = retained
receipt["source_helper_suppression_changes"] = suppression_changes
(root / "integration-repairs.json").write_text(json.dumps(receipt, indent=2) + "\n")
print("Restored unrelated selector formatting; retained", len(retained), "migrated selector simplifications and", len(suppression_changes), "source-helper corrections")
