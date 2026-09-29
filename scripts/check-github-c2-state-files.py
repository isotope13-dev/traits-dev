#!/usr/bin/env python3
"""Require a GitHub contents read before scoring C2 state-file markers."""

from pathlib import Path
import subprocess
import tempfile


RULE = "objectives/command-and-control/channel/deaddrop/github::github-c2-state-files"


def check(cleave: str, traits: Path, path: Path, expected: bool) -> None:
    result = subprocess.run(
        [cleave, "--traits-dir", str(traits), "test-rules", "--rules", RULE, str(path)],
        capture_output=True,
        text=True,
        check=True,
    )
    output = result.stdout + result.stderr
    marker = ("MATCHED " if expected else "NOT MATCHED ") + RULE + " (composite) "
    if not any(line.startswith(marker) for line in output.splitlines()):
        raise AssertionError(f"{path.name}: expected {marker.strip()}\n{output}")


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    cleave = str(root.parent / "cleave/target/release/cleave")
    with tempfile.TemporaryDirectory(prefix="github-c2-state-files-") as directory:
        temp = Path(directory)

        construct = temp / "construct-runtime.js"
        construct.write_text(
            'async function loadProject(runtime) { '
            'return runtime.assetManager.FetchJson("data.json"); }\n',
            encoding="utf-8",
        )
        check(cleave, root, construct, False)

        filenames_only = temp / "state-filenames-only.js"
        filenames_only.write_text(
            'const command = "cmd.json"; const data = "data.json"; '
            'const boot = "client_boot_id"; const sequence = "cmd_seq";\n',
            encoding="utf-8",
        )
        check(cleave, root, filenames_only, False)

        github_contents = temp / "github-contents-control.js"
        github_contents.write_text(
            'const owner = "example"; const repo = "control";\n'
            'const client = { async getJson(path) { '
            'const file = await fetch(`https://api.github.com/repos/${owner}/${repo}/contents/${path}`)'
            '.then(response => response.json()); '
            'return fromBase64Json(file.content); } };\n'
            'const command = "cmd.json"; const data = "data.json"; '
            'const boot = "client_boot_id"; const sequence = "cmd_seq";\n',
            encoding="utf-8",
        )
        check(cleave, root, github_contents, True)

    print("PASS GitHub C2 state files require a contents read and protocol markers")


if __name__ == "__main__":
    main()
