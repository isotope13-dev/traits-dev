"""Include the six initial corrections in the complete HEAD-to-final audit."""

import hashlib
import json
from pathlib import Path

root = Path(__file__).parent
repo = root.resolve().parents[2]
audit = json.loads((root / "item-placement-audit.json").read_text())
env = json.loads((root / "env-rule-audit.json").read_text())
mapping = json.loads((root / "item-id-map.json").read_text())
plan = {r["old_id"]: r for r in json.loads((root / "item-placement-plan.json").read_text())}
by_id = {r["old_id"]: r for r in audit["rules"]}
for row in env["rules"]:
    old = row["original_id"]
    lookup = old.replace("::javascript-npm-install-profile-http-get-exfil", "::npm-install-profile-near-raw-ip-http-get")
    row["final_id"] = mapping.get(lookup)
    if lookup in plan:
        row["rationale"] = plan[lookup]["reason"]
    if old != lookup and lookup in by_id:
        renamed = by_id.pop(lookup)
        renamed["old_id"] = old
        renamed["intermediate_id"] = lookup
        by_id[old] = renamed
    if old not in by_id and lookup not in by_id:
        by_id[old] = {"old_id": old, "new_id": None, "action": "remove-unsupported-claim", "reason": row["rationale"], "original_rule": row["original_rule"], "original_file": row["original_file"]}
    row["disposition"] = "removed-unsupported-claim" if row["final_id"] is None else "retained-observation-at-supported-item-or-capability"

notes = {
    "objectives/exfiltration/stealer/env::ruby-credential-env-http-request": "Replaced cross-language/source-only helper ORs with actual Ruby credential-source and canonical neutral HTTP POST observations.",
    "objectives/exfiltration/stealer/env::github-contents-credential-fallback": "Removed keyword-list and source-only branches; requires a credential exporter before adding GitHub-write context.",
    "objectives/exfiltration/stealer/env::native-forked-node-addon-form-env-http-exfil": "Removed the non-secret npm-install-profile branch from the credential-source alternatives.",
    "objectives/exfiltration/stealer/screen::page-content-payload-field": "Corrected double-escaped word/whitespace boundaries; a local-only page-cache control requires the neutral field observation and zero suspicious/hostile findings.",
    "objectives/exfiltration/stealer/screen::screenshot-payload-field": "Corrected double-escaped word/whitespace boundaries; field names remain neutral, without a capture/export claim.",
}
for old, note in notes.items():
    by_id[old]["predicate_or_level_change"] = note

audit["rules"] = sorted(by_id.values(), key=lambda r: r["old_id"])
audit["reviewed_after_initial_corrections"] = 1217
audit["reviewed"] = len(audit["rules"])
audit["removed_unsupported_claims"] = sum(r["new_id"] is None for r in audit["rules"])
audit["surviving_original_rules"] = len(mapping)
audit["new_rules"] = ["objectives/exfiltration/stealer/configuration/environment::javascript-environment-json-http-export"]
audit["retained_observations"] = sum(audit["counts"].values())
audit["stolen_item_rules"] = sum(n for directory, n in audit["counts"].items() if directory.startswith("objectives/exfiltration/stealer"))
audit["relocated_outside_theft"] = audit["retained_observations"] - audit["stolen_item_rules"]
assert audit["reviewed"] == 1223
assert audit["removed_unsupported_claims"] == 17
env["removed"] = sum(r["final_id"] is None for r in env["rules"])
assert env["count"] == 101 and env["removed"] == 8
(root / "item-placement-audit.json").write_text(json.dumps(audit, indent=2) + "\n")
(root / "env-rule-audit.json").write_text(json.dumps(env, indent=2) + "\n")

binary = repo.parent / "cleave/target/release/cleave"
engine_sources = [repo.parent / "cleave/src/capabilities" / p for p in (
    "validation/taxonomy.rs", "mapper/loader_directory.rs")]
rule_paths = sorted(p for tier in ("micro-behaviors", "objectives", "metadata", "well-known", "third-party") for p in (repo / tier).rglob("*") if p.suffix in (".yaml", ".yml", ".yar", ".yara") and p.is_file())
rule_digest = hashlib.sha256()
for path in rule_paths:
    rule_digest.update(str(path.relative_to(repo)).encode() + b"\0")
    rule_digest.update(hashlib.file_digest(path.open("rb"), "sha256").digest())
(root / "analysis-build.json").write_text(json.dumps({
    "binary": str(binary),
    "binary_sha256": hashlib.file_digest(binary.open("rb"), "sha256").hexdigest(),
    "engine_source_sha256": {str(p.relative_to(repo.parent / "cleave")): hashlib.file_digest(p.open("rb"), "sha256").hexdigest() for p in engine_sources},
    "build_log": "release-build-final.log",
    "unit_test_log": "item-placement-tests.log",
    "rule_source_files": len(rule_paths),
    "rule_sources_sha256": rule_digest.hexdigest(),
    "validation_log": "validate-fixtures.log",
}, indent=2) + "\n")
print("reviewed", audit["reviewed"], "removed", audit["removed_unsupported_claims"], "outside theft", audit["relocated_outside_theft"])
