#!/usr/bin/env python3
"""Check the Google Analytics page URL observation and its boundary."""

from pathlib import Path
import subprocess
import tempfile


RULE = "micro-behaviors/communications/http/services/analytics::google-analytics-pageview-url"


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
    with tempfile.TemporaryDirectory(prefix="google-analytics-pageview-") as directory:
        temp = Path(directory)
        positive = temp / "pageview.js"
        positive.write_text(
            'const endpoint = "https://www.google-analytics.com/mp/collect?'
            'measurement_id=G-EXAMPLE&api_secret=example";\n'
            'const event = {name:"page_view", params:{page_url: tab.url}};\n',
            encoding="utf-8",
        )
        check(cleave, root, positive, True)

        negative = temp / "pageview-without-url.js"
        negative.write_text(
            'const endpoint = "https://www.google-analytics.com/mp/collect?'
            'api_secret=example&measurement_id=G-EXAMPLE";\n'
            'const event = {name:"page_view", params:{page_host: tab.host}};\n',
            encoding="utf-8",
        )
        check(cleave, root, negative, False)

        missing_protocol_field = temp / "pageview-without-api-secret.js"
        missing_protocol_field.write_text(
            'const endpoint = "https://www.google-analytics.com/mp/collect?'
            'measurement_id=G-EXAMPLE";\n'
            'const event = {name:"page_view", params:{page_url: tab.url}};\n',
            encoding="utf-8",
        )
        check(cleave, root, missing_protocol_field, False)

    print("PASS GA page_view URL telemetry requires the endpoint, event, and URL field")


if __name__ == "__main__":
    main()
