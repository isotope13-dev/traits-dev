#!/usr/bin/env python3
"""Check API co-occurrence and locale module roles against attack controls."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]


def scan(cleave, *paths):
    result = subprocess.run(
        [cleave, "--traits-dir", str(ROOT), "--disable=rizin", "--json",
         *map(str, paths)], text=True, capture_output=True, check=True,
    )
    return [f for line in result.stdout.split("\n") if line
            for f in json.loads(line)["files"]]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cleave", default=str(ROOT.parent / "cleave/target/release/cleave"))
    args = parser.parse_args()
    notable = ROOT / "testdata/notable/generated/tar-triage"
    source_report = scan(args.cleave, notable / "socket-process-utility.c")[0]
    assert not [t for t in source_report["traits"] if t["crit"] >= 4], source_report
    with tempfile.TemporaryDirectory(prefix="tar-triage-regression-") as work:
        binary = Path(work) / "process-utility"
        subprocess.run(["cc", "-O0", str(notable / "socket-process-utility.c"),
                        "-o", str(binary)], check=True)
        report = scan(args.cleave, binary)[0]
        traits = {t["id"]: t for t in report["traits"]}
        required = {
            "metadata/file/profile/socket-runtime::connect-import",
            "micro-behaviors/process/fd/dup::dup2",
            "metadata/binary/symbols/name/process::execve-import",
            "micro-behaviors/fs/path/application/interpreter::bin-sh-path-reference",
        }
        assert required <= traits.keys(), required - traits.keys()
        assert not [t for t in traits.values() if t["crit"] >= 4], traits

    reverse_shell = ROOT / "testdata/hostile/generated/reverse-shell/revshell.cpp"
    assert any(t["crit"] == 5 for t in scan(args.cleave, reverse_shell)[0]["traits"])
    compressed = ROOT / "testdata/hostile/samples/reverse-shell.cpp.xz.xz"
    assert any(t["crit"] == 5 for f in scan(args.cleave, compressed) for t in f["traits"])

    paths = [notable / "vendor.js",
             ROOT / "testdata/hostile/generated/tar-triage/locale.js",
             ROOT / "testdata/suspicious/generated/taxonomy/stranded-members/locale-positive.js",
             ROOT / "testdata/notable/generated/taxonomy/stranded-members/locale-bundle.js"]
    reports = {Path(f["path"]).name: f for f in scan(args.cleave, *paths)}
    assert not [t for t in reports["locale-bundle.js"]["traits"] if t["crit"] >= 4]
    prefix = "objectives/supply-chain/trojanized/locale::"
    assert not [t for t in reports["vendor.js"]["traits"] if t["id"].startswith(prefix)]
    assert any(t["id"] == prefix + "trojanized-locale-resource"
               for t in reports["locale.js"]["traits"])
    assert any(t["id"] == prefix + "locale-resource-runtime-code-build"
               for t in reports["locale-positive.js"]["traits"])

    print("Tar triage regression checks passed")


if __name__ == "__main__":
    main()
