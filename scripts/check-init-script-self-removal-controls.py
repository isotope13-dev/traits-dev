#!/usr/bin/env python3
"""Check that init cleanup requires an executable update-rc.d command."""
import argparse
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RULE = "objectives/persistence/system/init/boot::init-script-self-removal"


def findings(binary: str, path: Path) -> set[str]:
    result = subprocess.run(
        [binary, "--traits-dir", str(ROOT), "--format", "json", str(path)],
        capture_output=True,
        text=True,
        check=True,
    )
    report = json.loads(result.stdout)
    return {
        trait["id"]
        for file in report["files"]
        for trait in file.get("traits", [])
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cleave", default="cleave")
    args = parser.parse_args()

    noop = ROOT / "testdata/taxonomy/init-script-self-removal/noop-argument.sh"
    actual = ROOT / "testdata/taxonomy/init-script-self-removal/actual-command.sh"
    noop_traits = findings(args.cleave, noop)
    assert RULE not in noop_traits, ("shell no-op argument was treated as a call", noop_traits)
    actual_traits = findings(args.cleave, actual)
    assert RULE in actual_traits, ("actual update-rc.d command was missed", actual_traits)
    print("init-script-self-removal controls: passed", flush=True)


if __name__ == "__main__":
    main()
