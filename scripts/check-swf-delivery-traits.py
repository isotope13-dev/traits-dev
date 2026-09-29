#!/usr/bin/env python3
"""Check that Flash delivery findings require SWF bytes, not incidental text."""

from pathlib import Path
import subprocess
import tempfile


def assert_match(cleave: str, traits: Path, path: Path, rule: str, expected: bool) -> None:
    result = subprocess.run(
        [cleave, "--traits-dir", str(traits), "test-rules", "--rules", rule, str(path)],
        capture_output=True,
        text=True,
        check=True,
    )
    output = result.stdout + result.stderr
    marker = ("MATCHED " if expected else "NOT MATCHED ") + rule + " "
    if not any(line.startswith(marker) for line in output.splitlines()):
        raise AssertionError(f"{path.name}: expected {marker.strip()}\n{output}")


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    cleave = str(root.parent / "cleave/target/release/cleave")
    rule = "objectives/command-and-control/dropper/delivery/flash::swf-http-url"

    with tempfile.TemporaryDirectory(prefix="swf-delivery-") as directory:
        temp = Path(directory)
        url = b"https://cdn.example.invalid/player.swf\0"
        target = b"player.swf\0"
        # Minimal uncompressed FWS header, zero-sized RECT, frame rate/count,
        # End tag, then URL and target strings.
        body = b"\0\0\x18\x01\0\0\0" + url + target
        swf = b"FWS\x09" + (8 + len(body)).to_bytes(4, "little") + body
        positive = temp / "movie.dat"
        positive.write_bytes(swf)
        assert_match(cleave, root, positive, rule, True)

        # Same kind of strings in ordinary source-like text must not identify
        # a Flash movie, even when a generic data suffix makes it scannable.
        negative = temp / "bundle.dat"
        negative.write_bytes(
            b'const player = "https://cdn.example.invalid/player.swf";\n'
        )
        assert_match(cleave, root, negative, rule, False)

    print("PASS SWF URL requires an FWS/CWS/ZWS content signature")


if __name__ == "__main__":
    main()
