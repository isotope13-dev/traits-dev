#!/usr/bin/env python3
"""Focused capability/intent boundaries and retained out-of-batch attacks."""
import argparse
import json
import pathlib
import subprocess


def read_reports(text):
    decoder = json.JSONDecoder()
    files = {}
    text = text.lstrip()
    while text:
        report, end = decoder.raw_decode(text)
        text = text[end:].lstrip()
        for file in report["files"]:
            files[file["path"]] = file
    return files


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cleave", default="cleave")
    parser.add_argument("--traits-dir", default=".")
    parser.add_argument("--before-traits")
    args = parser.parse_args()
    root = pathlib.Path(__file__).resolve().parents[3]
    cases = json.loads(pathlib.Path(__file__).with_name("cases.json").read_text())
    paths = [case["path"] for case in cases]

    def scan(traits):
        result = subprocess.run(
            [args.cleave, "--traits-dir", traits, "--format", "json", *paths],
            cwd=root, text=True, capture_output=True, check=True,
        )
        return read_reports(result.stdout)

    after = scan(args.traits_dir)
    for case in cases:
        report = after[case["path"]]
        traits = {t["id"]: t["crit"] for t in report.get("traits", [])}
        for trait in case.get("required", []):
            assert trait in traits, (case["path"], "missing", trait)
        for trait in case.get("forbidden", []):
            assert trait not in traits, (case["path"], "unexpected", trait)
        if "max_criticality" in case:
            assert max(traits.values(), default=0) <= case["max_criticality"], case["path"]

    if args.before_traits:
        before = scan(args.before_traits)
        for case in cases:
            if not case.get("preserve_attacks"):
                continue
            path = case["path"]
            old = {t["id"] for t in before[path].get("traits", []) if t["crit"] >= 4}
            new = {t["id"] for t in after[path].get("traits", []) if t["crit"] >= 4}
            assert old <= new, (path, "lost attack coverage", sorted(old - new))
    print(f"PASS: {len(cases)} focused cases; retained attack coverage checked")


if __name__ == "__main__":
    main()
