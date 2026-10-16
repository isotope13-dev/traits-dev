#!/usr/bin/env python3
"""Exercise file-scoped libpcap suppressors with copied and split clues."""
import argparse
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PATH_CLUE = "::source-tree-path"
HEADER_CLUE = "::pcap-int-header"
KMEM = "::c-kmem-device-open"

CASES = [
    {
        "id": "kmem-no-library-clue",
        "files": {"unrelated/kmem.c": "kmem.c"},
        "required": [KMEM],
        "forbidden": [PATH_CLUE, HEADER_CLUE],
    },
    {
        "id": "kmem-copied-pcap-sys-path-same-file",
        "files": {"pcap-sys-7/kmem.c": "kmem.c"},
        "required": [PATH_CLUE, KMEM],
        "forbidden": [],
    },
    {
        "id": "kmem-copied-libpcap-path-same-file",
        "files": {"libpcap/kmem.c": "kmem.c"},
        "required": [PATH_CLUE, KMEM],
        "forbidden": [],
    },
    {
        "id": "kmem-copied-header-same-file",
        "files": {"unrelated/kmem-with-header.c": "kmem-with-header.c"},
        "required": [HEADER_CLUE, KMEM],
        "forbidden": [],
    },
    {
        "id": "kmem-path-clue-in-sibling-does-not-suppress",
        "files": {
            "unrelated/kmem.c": "kmem.c",
            "pcap-sys-7/reference.c": "empty.c",
        },
        "required": [KMEM],
        "forbidden": [PATH_CLUE, HEADER_CLUE],
        "target": "kmem.c",
    },
    {
        "id": "kmem-header-clue-in-sibling-does-not-suppress",
        "files": {
            "unrelated/kmem.c": "kmem.c",
            "unrelated/reference.c": "header-marker.c",
        },
        "required": [KMEM],
        "forbidden": [PATH_CLUE, HEADER_CLUE],
        "target": "kmem.c",
    },
    {
        "id": "legacy-capture-no-library-clue",
        "files": {"unrelated/capture.c": "capture.c"},
        "required": [
            "::nit-device",
            "::promiscuous-capture-flag",
            "::nit-bind-ioctl",
            "::legacy-nit-sniffer",
            "::plaintext-credential-sniffer",
        ],
        "forbidden": [PATH_CLUE, HEADER_CLUE],
    },
    {
        "id": "legacy-capture-copied-path-same-file",
        "files": {"pcap-sys-7/capture.c": "capture.c"},
        "required": [PATH_CLUE,
            "::nit-device",
            "::promiscuous-capture-flag",
            "::nit-bind-ioctl",
            "::legacy-nit-sniffer",
            "::plaintext-credential-sniffer",
        ],
        "forbidden": [],
    },
    {
        "id": "legacy-capture-copied-header-same-file",
        "files": {"unrelated/capture-with-header.c": "capture-with-header.c"},
        "required": [HEADER_CLUE,
            "::nit-device",
            "::promiscuous-capture-flag",
            "::nit-bind-ioctl",
            "::legacy-nit-sniffer",
            "::plaintext-credential-sniffer",
        ],
        "forbidden": [],
    },
    {
        "id": "legacy-capture-header-clue-in-sibling-does-not-suppress",
        "files": {
            "unrelated/capture.c": "capture.c",
            "unrelated/reference.c": "header-marker.c",
        },
        "required": [
            "::nit-device",
            "::promiscuous-capture-flag",
            "::nit-bind-ioctl",
            "::legacy-nit-sniffer",
            "::plaintext-credential-sniffer",
        ],
        "forbidden": [PATH_CLUE, HEADER_CLUE],
        "target": "capture.c",
    },
    {
        "id": "legacy-capture-path-clue-in-sibling-does-not-suppress",
        "files": {
            "unrelated/capture.c": "capture.c",
            "pcap-sys-7/reference.c": "empty.c",
        },
        "required": [
            "::nit-device",
            "::promiscuous-capture-flag",
            "::nit-bind-ioctl",
            "::legacy-nit-sniffer",
            "::plaintext-credential-sniffer",
        ],
        "forbidden": [PATH_CLUE, HEADER_CLUE],
        "target": "capture.c",
    },
]

SOURCES = {
    "kmem.c": HERE / "kmem.c",
    "kmem-with-header.c": None,
    "capture.c": HERE / "capture.c",
    "capture-with-header.c": None,
    "header-marker.c": HERE / "header-marker.c",
    "empty.c": None,
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
    with tempfile.TemporaryDirectory(prefix="pcap-matrix-") as tmp:
        base = Path(tmp)
        all_paths = []
        case_paths = {}
        for case in CASES:
            case_paths[case["id"]] = []
            for relative, source_id in case["files"].items():
                path = base / case["id"] / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                if source_id in ("kmem-with-header.c", "capture-with-header.c"):
                    source = (HERE / source_id.replace("-with-header", "")).read_text()
                    path.write_text(source + '\n#include "pcap-int.h"\n')
                elif source_id == "empty.c":
                    path.write_text("int unrelated_reference(void) { return 0; }\n")
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
