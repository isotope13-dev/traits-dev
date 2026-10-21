"""Check placement and near misses using the full rule evaluator.

The rendered report can omit redundant grouping composites, so test-rules is
used to verify both those groups and their consuming credential rules.
"""
import argparse
import json
from pathlib import Path
import re
import subprocess


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cleave", default="cleave")
    parser.add_argument("--cases", type=Path, default=Path(__file__).with_name("cases.json"))
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[3]
    cases = json.loads(args.cases.read_text())["fixtures"]
    failures = []
    for case in cases:
        rules = case["matched"] + case["not_matched"]
        result = subprocess.run(
            [args.cleave, "--traits-dir", str(repo), "test-rules", case["path"],
             "--rules", ",".join(rules)],
            cwd=repo, capture_output=True, text=True, check=True,
        )
        if re.search(r"Warning: Rule .* not found", result.stdout + result.stderr) or "validation failed" in result.stderr:
            raise RuntimeError(result.stdout + result.stderr)
        matched = set(re.findall(r"^MATCHED (\S+)", result.stdout, re.MULTILINE))
        missing = set(case["matched"]) - matched
        unexpected = set(case["not_matched"]) & matched
        ok = not (missing or unexpected)
        print(("PASS " if ok else "FAIL ") + case["path"], flush=True)
        if not ok:
            failures.append({"path": case["path"], "missing": sorted(missing),
                             "unexpected": sorted(unexpected)})
    if failures:
        raise SystemExit(json.dumps(failures, indent=2))


if __name__ == "__main__":
    main()
