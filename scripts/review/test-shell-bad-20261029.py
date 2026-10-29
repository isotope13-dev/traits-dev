#!/usr/bin/env python3
"""Check shell triage technique variants and benign counterexamples."""
import argparse
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--atomscan", default="../scan/target/release/atomscan")
    parser.add_argument("--results", type=Path, help="verify an existing Atomscan JSONL report")
    args = parser.parse_args()
    cases = json.loads((Path(__file__).with_suffix(".json")).read_text())
    if args.results:
        data = args.results.read_text()
    else:
        env = dict(os.environ)
        env.setdefault("CLEAVE_TRAITS_DIR", str(ROOT))
        run = subprocess.run(
            [str(Path(args.atomscan).resolve()), "--no-update", "--analyze", "local",
             "--mode", "slow", "--follow=none", "--format=json", *cases],
            cwd=ROOT, env=env, capture_output=True, text=True,
        )
        if run.returncode not in (0, 1):
            raise SystemExit(run.stderr)
        data = run.stdout
    records = [json.loads(line) for line in data.split("\n") if line.startswith("{")]
    for path, case in cases.items():
        matching = [r for r in records if any(
            f["path"].endswith(path) for f in r.get("raw", {}).get("files", []))]
        assert len(matching) == 1, (path, "expected one report", len(matching))
        traits = {t["id"]: t["crit"] for f in matching[0]["raw"]["files"]
                  for t in f.get("traits", [])}
        assert not set(case["expected"]) - traits.keys(), (path, "missing", case["expected"])
        assert not set(case["absent"]) & traits.keys(), (path, "unexpected", case["absent"])
        severity = max(traits.values(), default=0)
        if case["level"] == "notable":
            assert severity < 4, (path, "benign counterexample has suspicious/hostile finding")
        elif case["level"] == "suspicious":
            assert severity == 4, (path, "expected suspicious finding")
        else:
            assert severity == 5, (path, "expected hostile finding")
    print(f"{len(cases)} shell triage regression cases passed")

if __name__ == "__main__":
    main()
