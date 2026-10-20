"""Static regression controls for complete Go filename literals vs path fragments."""
import argparse
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
PREFIX = "objectives/execution/exploit/command-injection::"
OLD = PREFIX + "filename-quote-shell-breakout-literal"
GO = PREFIX + "go-filename-quote-shell-breakout"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work-dir", required=True, type=Path)
    parser.add_argument("--cleave", default="cleave")
    args = parser.parse_args()
    args.work_dir.mkdir(parents=True, exist_ok=True)
    cases = {
        "raw-filename.go": ('package main\nvar name = `record.wav"; id`\n', GO),
        "escaped-filename.go": ('package main\nvar name = "record.wav\\\"& calc"\n', GO),
        "single-quote.go": ('package main\nvar name = "record.wav\'; id"\n', GO),
        "normal-filename.go": ('package main\nvar name = "record.wav"\n', None),
        "quoted-chain.go": (
            'package main\nvar command = `copy "file.db"; certutil -decode "file.db" "script.ps1"; echo ok`\n', None),
        "windows-paths.go": (
            'package main\nvar command = "copy \'C:\\\\Users\\\\Public\\\\file.db\'; '
            'certutil -decode \'C:\\\\Users\\\\Public\\\\file.db\' '
            '\'C:\\\\Users\\\\Public\\\\script.ps1\'; echo ok"\n', None),
        "comment.go": ('package main\n// name = `record.wav"; id`\n', None),
        "python-positive.py": ('name = \'record.wav"; id\'\n', OLD),
        "python-docstring.py": ('"""record.wav\'; id"""\n', None),
        "javascript-positive.js": ('const name = \'record.wav"; id\';\n', OLD),
    }
    paths = []
    for name, (source, _) in cases.items():
        path = args.work_dir / name
        path.write_text(source)
        paths.append(str(path))
    env = dict(os.environ)
    env.pop("CLEAVE_VALIDATE", None)
    result = subprocess.run(
        [args.cleave, "--traits-dir", str(ROOT), "--disable", "yara,third-party",
         "--format", "json", *paths],
        capture_output=True, text=True, env=env, check=True,
    )
    # Multiple inputs can produce adjacent JSON objects rather than one array.
    remaining = result.stdout.lstrip()
    decoder = json.JSONDecoder()
    found = {}
    while remaining:
        report, end = decoder.raw_decode(remaining)
        remaining = remaining[end:].lstrip()
        for file in report["files"]:
            found[Path(file["path"]).name] = {
                trait["id"] for trait in file.get("traits", [])
                if trait["id"] in (OLD, GO)
            }
    for name, (_, expected) in cases.items():
        wanted = {expected} if expected else set()
        assert found.get(name) == wanted, (name, wanted, found.get(name))
    print(f"Passed {len(cases)} filename-breakout controls")


if __name__ == "__main__":
    main()
