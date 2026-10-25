#!/usr/bin/env python3
"""Check neutral placement and word boundaries without running the fixtures."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cleave", default="cleave")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[3]
    source = Path(__file__).with_name("worker-name.c")
    cases = [
        ("_walker.worker.workerLoop", "worker-loop-name-token"),
        ("monitorWorker", "monitor-worker-name-token"),
        ("TaskLoop", "task-loop-name-token"),
        ("workerLooper monitorWorkers myTaskLoop", None),
    ]
    prefix = "metadata/binary/symbols/name/token::"
    expected_ids = {prefix + case[1] for case in cases if case[1]}
    with tempfile.TemporaryDirectory(prefix="worker-name-placement-") as temp:
        paths = []
        for index, (name, _) in enumerate(cases):
            target = Path(temp) / f"case-{index}.o"
            subprocess.run([
                "cc", "-c", str(source), f'-DWORKER_NAME="{name}"',
                "-o", str(target),
            ], check=True)
            paths.append(target)
        result = subprocess.run([
            args.cleave, "--traits-dir", str(root), "--disable", "radare2",
            "--format", "json", "analyze", *map(str, paths),
        ], check=True, capture_output=True, text=True)
        decoder = json.JSONDecoder()
        remaining = result.stdout.lstrip()
        files = []
        while remaining:
            document, end = decoder.raw_decode(remaining)
            files.extend(document.get("files", []))
            remaining = remaining[end:].lstrip()
        by_path = {Path(item["path"]): item for item in files}
        for path, (name, token) in zip(paths, cases):
            traits = by_path[path].get("traits", [])
            ids = {trait["id"] for trait in traits}
            expected = {prefix + token} if token else set()
            assert ids & expected_ids == expected, (name, ids & expected_ids)
            # Cleave filters bare any-of composites from emitted findings;
            # their constituent atoms remain available to C2 consumers.
            assert not any("::go-monitor-worker" in item for item in ids), name
            assert not any(trait.get("crit", 0) >= 4 for trait in traits), name
    print("worker-name placement: 4 controls passed")


if __name__ == "__main__":
    main()
