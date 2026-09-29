#!/usr/bin/env python3
"""Check page_visit URL telemetry and the boundary for a missing URL field."""

from pathlib import Path
import subprocess
import tempfile


RULE = "micro-behaviors/os/telemetry/activity::page-visit-url-field"


def check(cleave: str, traits: Path, path: Path, expected: bool) -> None:
    result = subprocess.run(
        [cleave, "--traits-dir", str(traits), "test-rules", "--rules", RULE, str(path)],
        capture_output=True,
        text=True,
        check=True,
    )
    output = result.stdout + result.stderr
    marker = ("MATCHED " if expected else "NOT MATCHED ") + RULE + " "
    if not any(line.startswith(marker) for line in output.splitlines()):
        raise AssertionError(f"{path.name}: expected {marker.strip()}\n{output}")


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    cleave = str(root.parent / "cleave/target/release/cleave")
    with tempfile.TemporaryDirectory(prefix="page-visit-url-") as directory:
        temp = Path(directory)
        positive = temp / "page-visit.js"
        positive.write_text(
            'track("page_visit", {platform: "chatgpt", url: location.href, '
            'visit_time: Date.now()});\n',
            encoding="utf-8",
        )
        check(cleave, root, positive, True)

        negative = temp / "page-visit-without-url.js"
        negative.write_text(
            'track("page_visit", {platform: "chatgpt", visit_time: Date.now()});\n',
            encoding="utf-8",
        )
        check(cleave, root, negative, False)

    print("PASS page_visit telemetry requires a URL field")


if __name__ == "__main__":
    main()
