"""Check content without accidentally activating test-directory exclusions."""

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cleave", default="cleave")
    parser.add_argument("--work-dir", required=True)
    args = parser.parse_args()
    base = Path(__file__).resolve().parent
    root = base.parents[2]
    cases = json.loads((base / "cases.json").read_text())["fixtures"]
    with tempfile.TemporaryDirectory(prefix="ty-controls-", dir=args.work_dir) as tmp:
        staged = {}
        for case in cases:
            source = root / case["path"]
            target = Path(tmp) / source.relative_to(base)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
            staged[str(target)] = case
        result = subprocess.run(
            [args.cleave, "--traits-dir", str(root), "--format", "jsonl", *staged],
            check=True,
            text=True,
            capture_output=True,
        )
        if result.stderr.strip():
            raise AssertionError(result.stderr)
        seen = set()
        files = []
        text = result.stdout.strip()
        decoder = json.JSONDecoder()
        while text:
            report, end = decoder.raw_decode(text)
            files.extend(report["files"])
            text = text[end:].lstrip()
        for file in files:
            if file["path"] not in staged:
                continue
            case = staged[file["path"]]
            seen.add(file["path"])
            traits = {trait["id"] for trait in file.get("traits", [])}
            missing = set(case["matched"]) - traits
            unexpected = set(case["not_matched"]) & traits
            assert not missing, (case["path"], "missing", sorted(missing))
            assert not unexpected, (case["path"], "unexpected", sorted(unexpected))
        assert seen == set(staged), ("unscanned controls", set(staged) - seen)
    print(f"PASS: {len(cases)} positive and near-miss controls")


if __name__ == "__main__":
    main()
