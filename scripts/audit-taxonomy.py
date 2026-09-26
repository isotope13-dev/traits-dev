#!/usr/bin/env python3
"""Inventory taxonomy size, sibling scope, references, and matcher overlaps.

Requires PyYAML. This is an audit report, not a replacement for cleave validate.
Run: python3 scripts/audit-taxonomy.py --out /tmp/taxonomy-audit
"""

import argparse
import csv
import json
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path

TIERS = ("metadata", "micro-behaviors", "objectives", "well-known")
LAYER_TERMS = frozenset((
    "library", "lib", "framework", "wrapper", "provider", "implementation",
    "stdlib", "runtime", "api", "helper", "helpers", "binding", "bindings",
    "bridge", "sdk", "tool", "tools",
))


def inventory(root):
    import yaml

    counts = defaultdict(lambda: [0, 0])
    rules = []
    for tier in TIERS:
        for path in sorted((root / tier).rglob("*")):
            if path.suffix not in (".yaml", ".yml"):
                continue
            data = yaml.safe_load(path.read_text()) or {}
            directory = str(path.parent.relative_to(root))
            for index, kind in enumerate(("traits", "composite_rules")):
                for rule in data.get(kind, []) or []:
                    counts[directory][index] += 1
                    rules.append(dict(file=str(path.relative_to(root)),
                                      directory=directory, kind=kind,
                                      defaults=data.get("defaults", {}), rule=rule))
    return dict(counts=dict(counts), rules=rules)


def write_csv(out, name, fields, rows):
    with (out / name).open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def references(node):
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "id" and isinstance(value, str):
                yield value
            else:
                yield from references(value)
    elif isinstance(node, list):
        for value in node:
            yield from references(value)


def audit_layers(data, out, revision):
    """Find vocabulary for semantic review; names alone are not violations."""
    out.mkdir(parents=True, exist_ok=True)
    counts, rules = data["counts"], data["rules"]
    nodes = set(counts)
    for directory in counts:
        nodes.update(str(p) for p in Path(directory).parents if len(p.parts) > 1)
    candidates = {}
    for directory in sorted(nodes):
        segment = Path(directory).name
        terms = sorted(set(re.split(r"[-_]", segment)) & LAYER_TERMS)
        if terms:
            candidates[directory] = dict(
                directory=directory, terms=";".join(terms),
                name_match="exact" if segment in LAYER_TERMS else "compound",
                depth=len(Path(directory).parts) - 1,
                direct_atomic=counts.get(directory, [0, 0])[0],
                direct_composite=counts.get(directory, [0, 0])[1],
                subtree_rules=0, leaves=set(), files=set(), samples={})
    for record in rules:
        path = Path(record["directory"])
        for directory in [str(path), *(str(p) for p in path.parents)]:
            if directory not in candidates:
                continue
            row = candidates[directory]
            row["subtree_rules"] += 1
            row["leaves"].add(record["directory"])
            row["files"].add(record["file"])
            row["samples"].setdefault(record["directory"], record)
    rows = []
    for row in candidates.values():
        # One example per leaf, up to three, makes internal-node samples explicit.
        samples = row.pop("samples")
        examples = [samples[d] for d in sorted(samples)[:3]]
        row["rule_leaves"] = len(row.pop("leaves"))
        row["source_files"] = len(row.pop("files"))
        row["example_traits"] = ";".join(r["directory"] + "::" + r["rule"]["id"] for r in examples)
        row["example_files"] = ";".join(dict.fromkeys(r["file"] for r in examples))
        rows.append(row)
    fields = ("directory", "terms", "name_match", "depth", "direct_atomic",
              "direct_composite", "subtree_rules", "rule_leaves", "source_files",
              "example_traits", "example_files")
    write_csv(out, "layer-inventory.csv", fields, rows)
    summary = dict(revision=revision, rules=len(rules), rule_directories=len(counts),
                   vocabulary=sorted(LAYER_TERMS), candidate_nodes=len(rows),
                   exact_nodes=sum(r["name_match"] == "exact" for r in rows),
                   compound_nodes=sum(r["name_match"] == "compound" for r in rows),
                   outside_well_known=sum(not r["directory"].startswith("well-known/") for r in rows),
                   by_tier=dict(sorted(Counter(r["directory"].split("/")[0] for r in rows).items())),
                   note="Vocabulary inventory, not validation warnings. Nested subtree counts overlap; semantic review is required.")
    (out / "layer-summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    return summary


def audit(data, out, cap, revision):
    out.mkdir(parents=True, exist_ok=True)
    counts, rules = data["counts"], data["rules"]
    violating = {d for d, pair in counts.items() if sum(pair) > cap}
    parents = {str(Path(d).parent) for d in violating}
    # Collapse nested scopes, but include every sibling's descendants.
    scopes = sorted(p for p in parents if not any(p.startswith(q + "/") for q in parents if p != q))
    scoped = {d for d in counts if any(d == p or d.startswith(p + "/") for p in scopes)}
    by_directory = defaultdict(list)
    for record in rules:
        by_directory[record["directory"]].append(record)

    rows = []
    for directory in sorted(scoped):
        atomic, composite = counts[directory]
        rows.append(dict(directory=directory, atomic=atomic, composite=composite,
                         total=atomic + composite, excess=max(0, atomic + composite - cap),
                         depth=len(Path(directory).parts) - 1,
                         files=len({r["file"] for r in by_directory[directory]})))
    fields = ("directory", "atomic", "composite", "total", "excess", "depth", "files")
    write_csv(out, "siblings.csv", fields, rows)
    write_csv(out, "oversized.csv", fields,
              sorted((r for r in rows if r["excess"]), key=lambda r: (-r["total"], r["directory"])))

    # Identical if blocks are review candidates only. File/platform scope,
    # thresholds, exclusions, defaults, severity, and confidence can differ.
    matchers = defaultdict(list)
    for record in rules:
        condition = record["rule"].get("if")
        if record["kind"] == "traits" and isinstance(condition, dict) and "id" not in condition:
            matchers[json.dumps(condition, sort_keys=True)].append(record)
    overlaps = [group for group in matchers.values()
                if len(group) > 1 and any(r["directory"] in violating for r in group)]
    overlaps.sort(key=lambda group: min(r["directory"] + "::" + r["rule"]["id"] for r in group))
    duplicate_rows = []
    for index, group in enumerate(overlaps, 1):
        for record in sorted(group, key=lambda r: (r["directory"], r["rule"]["id"], r["file"])):
            effective = dict(record["defaults"] or {})
            effective.update(record["rule"])
            duplicate_rows.append(dict(group=index,
                trait=record["directory"] + "::" + record["rule"]["id"],
                file=record["file"], matcher=json.dumps(effective["if"], sort_keys=True),
                scope_and_constraints=json.dumps({k: v for k, v in effective.items()
                    if k not in ("id", "desc", "if", "mbc", "attack")}, sort_keys=True)))
    write_csv(out, "matcher-overlaps.csv",
              ("group", "trait", "file", "matcher", "scope_and_constraints"), duplicate_rows)

    exact = defaultdict(set)
    directory_refs = defaultdict(set)
    for record in rules:
        body = {k: v for k, v in record["rule"].items() if k != "id"}
        owner = record["directory"] + "::" + record["rule"]["id"]
        for ref in set(references(body)):
            if "::" in ref:
                exact[ref.split("::", 1)[0]].add(owner)
            elif "/" in ref:
                directory_refs[ref.rstrip("/")].add(owner)
            else:
                exact[record["directory"]].add(owner)
    impact = []
    for directory in sorted(violating):
        prefixes = [str(p) for p in Path(directory).parents if str(p) != "."] + [directory]
        broad = set().union(*(directory_refs[p] for p in prefixes))
        impact.append(dict(directory=directory, named_reference_owners=len(exact[directory]),
                           directory_reference_owners=len(broad),
                           directory_reference_prefixes=";".join(p for p in prefixes if directory_refs[p])))
    write_csv(out, "reference-impact.csv",
              ("directory", "named_reference_owners", "directory_reference_owners", "directory_reference_prefixes"), impact)

    children = defaultdict(set)
    for directory in counts:
        path = Path(directory)
        for parent in path.parents:
            if str(parent) != ".":
                children[str(parent)].add(path.relative_to(parent).parts[0])
    structure = []
    for directory in sorted(set(counts) | set(children)):
        depth, fanout = len(Path(directory).parts) - 1, len(children[directory])
        flags = []
        if directory in counts and depth > 4:
            flags.append("depth-above-four")
        if fanout == 1:
            flags.append("single-child-review")
        if fanout >= 90:
            flags.append("broad-parent-review")
        if directory in counts and fanout:
            flags.append("mixed-leaf")
        if flags:
            structure.append(dict(directory=directory, depth=depth, children=fanout,
                                  rules=sum(counts.get(directory, (0, 0))), flags=";".join(flags)))
    write_csv(out, "structure.csv", ("directory", "depth", "children", "rules", "flags"), structure)
    summary = dict(revision=revision, combined_cap=cap, exemptions=[],
                   files=len({r["file"] for r in rules}), rules=len(rules),
                   atomic=sum(c[0] for c in counts.values()), composite=sum(c[1] for c in counts.values()),
                   rule_directories=len(counts), violating_directories=len(violating),
                   rules_in_violators=sum(sum(counts[d]) for d in violating),
                   excess_rules=sum(sum(counts[d]) - cap for d in violating),
                   old_atomic_75_violations=sum(c[0] > 75 for c in counts.values()),
                   intermediate_combined_80_violations=sum(sum(c) > 80 for c in counts.values()),
                   violations_by_tier=dict(sorted(Counter(d.split("/")[0] for d in violating).items())),
                   sibling_scope_directories=len(scoped), sibling_scope_rules=sum(sum(counts[d]) for d in scoped),
                   sibling_scope_roots=scopes, matcher_overlap_groups=len(overlaps),
                   matcher_overlap_rules=len(duplicate_rows),
                   depths=dict(sorted(Counter(len(Path(d).parts) - 1 for d in counts).items())))
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--cap", type=int, default=85)
    parser.add_argument("--layers-only", action="store_true",
                        help="Only inventory implementation/resource vocabulary for semantic review")
    args = parser.parse_args()
    if args.cap < 1:
        parser.error("--cap must be positive")
    revision = subprocess.check_output(["git", "-C", str(args.root), "rev-parse", "HEAD"], text=True).strip()
    data = inventory(args.root)
    if args.layers_only:
        summary = audit_layers(data, args.out, revision)
    else:
        summary = audit(data, args.out, args.cap, revision)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
