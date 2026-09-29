#!/usr/bin/env python3
"""Check that octet-stream type alone does not imply registry publication."""

from pathlib import Path
import subprocess
import tempfile


RULE = "objectives/supply-chain/credential-theft/registry::rubygems-token-publish-upload"


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
    with tempfile.TemporaryDirectory(prefix="rubygems-octet-stream-") as directory:
        temp = Path(directory)
        positive = temp / "publish.js"
        positive.write_text(
            'const token = "rubygems_0123456789abcdefghijklmnopqrstuvwxyz";\n'
            'fetch("https://rubygems.org/api/v1/gems", {method:"PUT", '
            'headers:{"Content-Type":'
            '"application/octet-stream"}, body:archive});\n',
            encoding="utf-8",
        )
        check(cleave, root, positive, True)

        negative = temp / "generic-helper.js"
        negative.write_text(
            'if (body instanceof Blob || body instanceof ArrayBuffer) {\n'
            '  headers["Content-Type"] = "application/octet-stream";\n'
            '  requestBody = body;\n'
            '}\n',
            encoding="utf-8",
        )
        check(cleave, root, negative, False)

    print("PASS RubyGems publication requires registry, token, body-type, and request evidence")


if __name__ == "__main__":
    main()
