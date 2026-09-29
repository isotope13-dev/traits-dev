#!/usr/bin/env python3
"""Inventory the legacy dropper/execution subtree for manual sink review.

Run with: uv run --with pyyaml python3 scripts/audit-dropper-execution.py
The inventory records evidence and source paths; it does not infer activation
from names or from unrelated conditions in the same file.
"""

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "objectives/command-and-control/dropper/execution"
OUTPUT = ROOT / "docs/taxonomy-audit"


def references(node):
    """Return explicit referenced rule IDs, including nested conditions."""
    if isinstance(node, dict):
        found = [node["id"]] if isinstance(node.get("id"), str) else []
        for key, value in node.items():
            if key != "id":
                found.extend(references(value))
        return found
    if isinstance(node, list):
        return [ref for part in node for ref in references(part)]
    return []


def main():
    rows = []
    by_directory = defaultdict(Counter)
    body_groups = defaultdict(list)
    matcher_groups = defaultdict(list)
    for path in sorted(SOURCE.rglob("*.yaml")):
        document = yaml.safe_load(path.read_text()) or {}
        relative = path.relative_to(ROOT).as_posix()
        directory = path.parent.relative_to(SOURCE).as_posix()
        defaults = document.get("defaults") or {}
        for section in ("traits", "composite_rules"):
            for rule in document.get(section, []) or []:
                kind = "atomic" if section == "traits" else "composite"
                body = {key: value for key, value in rule.items()
                        if key not in ("id", "desc", "crit", "conf", "attack", "mbc")}
                effective_scope = {key: rule.get(key, defaults.get(key))
                                   for key in ("for", "platforms", "arch")}
                row = {
                    "directory": directory,
                    "id": f"objectives/command-and-control/dropper/execution/{directory}::{rule['id']}",
                    "kind": kind,
                    "crit": rule.get("crit", defaults.get("crit", "")),
                    "description": rule.get("desc", ""),
                    "file": relative,
                    "references": ";".join(references({key: rule[key] for key in
                        ("all", "any", "not", "unless", "needs", "ref") if key in rule})),
                    "matcher": json.dumps(rule.get("if", ""), sort_keys=True),
                    "effective_scope": json.dumps(effective_scope, sort_keys=True),
                }
                rows.append(row)
                by_directory[directory][kind] += 1
                # This is a candidate duplicate only: local IDs can resolve to
                # different definitions, and effective filters must be checked.
                body_groups[(kind, json.dumps(body, sort_keys=True),
                             row["effective_scope"])].append(row["id"])
                if "if" in rule:
                    matcher_groups[json.dumps(rule["if"], sort_keys=True)].append(row["id"])

    OUTPUT.mkdir(parents=True, exist_ok=True)
    inventory = OUTPUT / "dropper-execution-rules.csv"
    fieldnames = [
        "directory", "id", "kind", "crit", "description", "file",
        "references", "matcher", "effective_scope",
    ]
    with inventory.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    summary = {
        "files": len(list(SOURCE.rglob("*.yaml"))),
        "rules": len(rows),
        "directories": len(by_directory),
        "over_cap": {name: dict(counts) for name, counts in by_directory.items()
                     if sum(counts.values()) > 100},
        "by_directory": {name: dict(counts) for name, counts in sorted(by_directory.items())},
        "candidate_duplicate_bodies": [ids for ids in body_groups.values() if len(ids) > 1],
        "same_matcher_candidates": [ids for ids in matcher_groups.values() if len(ids) > 1],
    }
    (OUTPUT / "dropper-execution-summary.json").write_text(
        json.dumps(summary, indent=2) + "\n")
    print(f"{summary['files']} files, {len(rows)} rules, "
          f"{len(by_directory)} directories, {len(summary['over_cap'])} over cap")


if __name__ == "__main__":
    main()
