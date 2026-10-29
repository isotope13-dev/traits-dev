#!/usr/bin/env python3
"""Reject retired process subtrees, even when using an older cleave binary."""

import argparse
import json
from pathlib import Path

POLICY = Path(__file__).with_name("process-taxonomy-policy.json")


def violations(root, policy):
    for retired, guidance in policy.items():
        path = root / retired
        if path.is_dir():
            count = sum(1 for item in path.rglob("*") if item.is_file() and item.suffix in (".yaml", ".yml"))
            yield (
                f"{retired}: retired process category ({count} YAML files). "
                f"{guidance['reason']}\n  Destinations: "
                + ", ".join(guidance["destinations"])
            )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--traits-dir", type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args()
    policy = json.loads(POLICY.read_text())
    errors = list(violations(args.traits_dir, policy))
    if errors:
        print("\n".join(errors))
        return 1
    print(f"Process taxonomy: {len(policy)} retired subtrees absent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
