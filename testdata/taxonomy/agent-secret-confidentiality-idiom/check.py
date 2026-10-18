"""Run controls outside testdata so production test-corpus exclusions cannot mask failures."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--scratch", required=True)
    parser.add_argument("--cleave", default="cleave")
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    root = here.parents[2]
    cases = json.loads((here / "cases.json").read_text())["fixtures"]
    with tempfile.TemporaryDirectory(prefix="agent-wording-", dir=args.scratch) as temp:
        targets = []
        for case in cases:
            target = Path(temp) / Path(case["path"]).name
            shutil.copyfile(root / case["path"], target)
            targets.append(str(target))
        result = subprocess.run(
            [args.cleave, "--traits-dir", str(root), "--format", "json", *targets],
            check=True, capture_output=True, text=True,
        )
        # Multi-target output contains concatenated report objects.
        decoder = json.JSONDecoder()
        remaining = result.stdout
        files = {}
        while remaining.strip():
            remaining = remaining.lstrip()
            report, end = decoder.raw_decode(remaining)
            for file in report["files"]:
                files[Path(file["path"]).name] = {t["id"] for t in file.get("traits", [])}
            remaining = remaining[end:]
        for case in cases:
            name = Path(case["path"]).name
            actual = files[name]
            missing = set(case["matched"]) - actual
            unexpected = set(case["not_matched"]) & actual
            assert not missing and not unexpected, (name, missing, unexpected)
            print("PASS", name)


if __name__ == "__main__":
    main()
