"""Run static trait controls; never execute the analyzed fixtures."""
import argparse
import json
from pathlib import Path
import subprocess


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cleave", default="cleave")
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    root = here.parents[2]
    cases = json.loads((here / "cases.json").read_text())["fixtures"]
    for case in cases:
        result = subprocess.run(
            [args.cleave, "--traits-dir", str(root), "--format", "json",
             str(here / case["path"])],
            check=True, capture_output=True, text=True,
        )
        report = json.loads(result.stdout)
        traits = [t for f in report["files"] for t in f.get("traits", [])]
        observed = {t["id"] for t in traits}
        missing = set(case["matched"]) - observed
        unexpected = set(case["not_matched"]) & observed
        excessive = [t["id"] for t in traits if t["crit"] > case["max_crit"]]
        assert not (missing or unexpected or excessive), (
            case["path"], missing, unexpected, excessive,
        )
        print("PASS", case["path"])


if __name__ == "__main__":
    main()
