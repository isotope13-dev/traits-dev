#!/usr/bin/env python3
"""Google API-key header evidence stays neutral unless proxy context combines."""

import argparse
from pathlib import Path
import shutil
import subprocess
import tempfile
import zipfile


def main():
    root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cleave", default=str(root.parent / "cleave/target/release/cleave"))
    args = parser.parse_args()
    header = "micro-behaviors/communications/http/authorization-header::x-goog-api-key-header-map-entry"
    proxy = "objectives/exfiltration/http/agent::agent-skill-banana-proxy-credential-relay"
    expected = {
        "ordinary-provider-request.js": {header: True, proxy: False},
        "banana-skill.zip": {proxy: True},
    }

    for name, rules in expected.items():
        with tempfile.TemporaryDirectory(prefix="google-api-key-header-") as directory:
            target = Path(directory) / name
            fixture_dir = root / "testdata/taxonomy/google-api-key-header"
            if name == "banana-skill.zip":
                with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED) as archive:
                    archive.write(fixture_dir / "SKILL.md", "SKILL.md")
                    archive.write(fixture_dir / "proxy.js", "proxy.js")
            else:
                shutil.copyfile(fixture_dir / name, target)
            result = subprocess.run(
                [args.cleave, "--traits-dir", str(root), "test-rules", "--rules",
                 ",".join(rules), str(target)],
                capture_output=True,
                text=True,
                check=True,
            )
        output = result.stdout + result.stderr
        for rule, matched in rules.items():
            marker = ("MATCHED " if matched else "NOT MATCHED ") + rule + " "
            if not any(line.startswith(marker) for line in output.splitlines()):
                raise AssertionError(f"{name}: expected {marker.strip()}\n{output}")
        print(f"PASS {name}: {len(rules)} finding assertions", flush=True)


if __name__ == "__main__":
    main()
