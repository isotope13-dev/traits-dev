#!/usr/bin/env python3
"""Reject retired process subtrees, even when using an older cleave binary."""

import argparse
import json
import re
from pathlib import Path

POLICY = Path(__file__).with_name("process-taxonomy-policy.json")


def violations(root, policy):
    for retired, guidance in policy.items():
        path = root / retired
        if path.is_dir():
            count = sum(1 for item in path.rglob("*") if item.is_file() and item.suffix in (".yaml", ".yml"))
            destinations = guidance["destinations"]
            advice = ", ".join(destinations) if destinations else "choose a current home for each evidenced behavior"
            yield (
                f"{retired}: retired process category ({count} YAML files). "
                f"{guidance['reason']}\n  Destinations: "
                + advice
            )


REFERENCE = re.compile(r"^\s*(?:-\s*)?id:\s*['\"]?([^\s'\"#]+)")


def retired_references(root, policy):
    # IDs in comments or ordinary text are not live dependencies. Match YAML
    # id fields and compare path components so similarly named siblings remain
    # valid. Directory references and explicit trait IDs are both covered.
    retired = set(policy)
    for tier in ("micro-behaviors", "metadata", "objectives", "well-known"):
        base = root / tier
        if not base.is_dir():
            continue
        for path in base.rglob("*"):
            if not path.is_file() or path.suffix not in (".yaml", ".yml"):
                continue
            for number, line in enumerate(path.read_text().splitlines(), 1):
                match = REFERENCE.match(line)
                if not match:
                    continue
                reference = match.group(1).split("::", 1)[0].rstrip("/")
                parts = reference.split("/")
                for length in range(1, len(parts) + 1):
                    candidate = "/".join(parts[:length])
                    if candidate in retired:
                        yield f"{path.relative_to(root)}:{number}: references retired process category {candidate}: {match.group(1)}"
                        break


def invalid_destinations(root, policy):
    for retired, guidance in policy.items():
        for destination in guidance["destinations"]:
            if not (root / destination).is_dir() or any(
                destination == other or destination.startswith(other + "/")
                for other in policy
            ):
                yield f"{retired}: policy suggests unavailable or retired destination {destination}"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--traits-dir", type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args()
    policy = json.loads(POLICY.read_text())
    errors = list(violations(args.traits_dir, policy))
    errors.extend(retired_references(args.traits_dir, policy))
    errors.extend(invalid_destinations(args.traits_dir, policy))
    if errors:
        print("\n".join(errors))
        return 1
    print(f"Process taxonomy: {len(policy)} retired subtrees and live references absent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
