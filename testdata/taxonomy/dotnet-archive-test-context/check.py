#!/usr/bin/env python3
"""Exercise file-scoped test-tree suppression of the C2 archive trait."""
import argparse
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
C2_ARCHIVE = "::dotnet-c2-archive-base64"
# The base64 call itself, required so a suppressed case still proves the file
# was analyzed (the test-directory leg that gates the suppressor is stripped
# from scan output as low-tier).
BASE64_CALL = "::dotnet-to-base64string"

CASES = [
    {
        "id": "archive-in-test-tree-suppressed",
        "files": {"tests/archive-fixture.cs": "archive-fixture.cs"},
        "required": [BASE64_CALL],
        "forbidden": [C2_ARCHIVE],
    },
    {
        "id": "archive-outside-test-tree-fires",
        "files": {"src/archive-stager.cs": "archive-stager.cs"},
        "required": [C2_ARCHIVE, BASE64_CALL],
        "forbidden": [],
    },
    {
        "id": "test-clue-in-sibling-does-not-suppress",
        "files": {
            "src/archive-stager.cs": "archive-stager.cs",
            "tests/reference.cs": "empty.cs",
        },
        "required": [C2_ARCHIVE],
        "forbidden": [],
        "target": "archive-stager.cs",
    },
]

SOURCES = {
    "archive-fixture.cs": HERE / "archive-fixture.cs",
    "archive-stager.cs": HERE / "archive-stager.cs",
    "empty.cs": None,
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cleave", default=str(ROOT.parent / "cleave/target/release/cleave"))
    parser.add_argument("--record", type=Path)
    parser.add_argument("--quiet", action="store_true", help="print only the pass summary")
    args = parser.parse_args()
    cleave = shutil.which(args.cleave)
    assert cleave, f"Missing Cleave executable: {args.cleave}"
    cmd = [str(Path(cleave).resolve()), "--no-update-check", "--traits-dir", str(ROOT),
           "--disable", "yara,radare2,upx", "--format", "json"]
    env = {**os.environ, "CLEAVE_SKIP_CACHE": "1"}
    observed = {}
    with tempfile.TemporaryDirectory(prefix="dotnet-archive-matrix-") as tmp:
        base = Path(tmp)
        all_paths = []
        case_paths = {}
        for case in CASES:
            case_paths[case["id"]] = []
            for relative, source_id in case["files"].items():
                path = base / case["id"] / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                if source_id == "empty.cs":
                    path.write_text("namespace Fixture { }\n")
                else:
                    path.write_bytes(SOURCES[source_id].read_bytes())
                all_paths.append(str(path))
                case_paths[case["id"]].append(path)
        output = subprocess.run([*cmd, *all_paths], text=True, capture_output=True,
                                check=True, env=env)
        decoder = json.JSONDecoder()
        reports = []
        cursor = 0
        while cursor < len(output.stdout):
            while cursor < len(output.stdout) and output.stdout[cursor].isspace():
                cursor += 1
            if cursor == len(output.stdout):
                break
            item, cursor = decoder.raw_decode(output.stdout, cursor)
            reports.extend(item.get("files", []))
        by_path = {Path(item["path"]): item for item in reports}
        for case in CASES:
            target = case.get("target")
            selected = next((p for p in case_paths[case["id"]]
                             if target is None or p.name == target), case_paths[case["id"]][0])
            report = by_path[selected]
            found = {trait["id"] for trait in report.get("traits", [])}
            for rid in case["required"]:
                assert any(item.endswith(rid) for item in found), (case["id"], "missing", rid, sorted(found))
            for rid in case["forbidden"]:
                assert not any(item.endswith(rid) for item in found), (case["id"], "unexpected", rid, sorted(found))
            observed[case["id"]] = {
                "target": str(selected.relative_to(base)),
                "required_present": case["required"],
                "forbidden_absent": case["forbidden"],
                "emitted": sorted(found),
            }
        evidence = {"cleave_argv": [*cmd, *all_paths], "cases": observed}
        if args.record:
            args.record.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n")
        print(f"taxonomy matrix passed: {len(CASES)} cases; {len(all_paths)} files")
        if not args.quiet:
            print(f"command: {json.dumps([*cmd, *all_paths])}")
            print(json.dumps(observed, indent=2, sort_keys=True))
        if output.stderr and not args.quiet:
            print("stderr:")
            print(output.stderr, end="")


if __name__ == "__main__":
    main()
