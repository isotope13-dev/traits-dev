"""Near miss: a CLI hint that mentions ignore rules, not an agent override."""


def warn_stale_graph(changed: bool) -> None:
    if changed:
        print("  (ignore rules or filters changed?)")
