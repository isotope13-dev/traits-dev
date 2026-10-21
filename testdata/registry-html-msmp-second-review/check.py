#!/usr/bin/env python3
"""Check remote-include admission and module-buffer binding; never run samples."""
import argparse
import json
from pathlib import Path
import struct
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
SELF_DELETE = "objectives/evasion/self-delete/file/script::x86-module-path-retry-delete-batch"
MASS = "micro-behaviors/process/deploy/script-eval::massed-remote-script-tags"
HOSTILE = {
    "objectives/persistence/login/registry/autostart::msmp-state-loader-windows-run-persistence",
    "well-known/malware/trojan/urelas::urelas-msmp-network-loader",
}


def scan(engine, paths):
    run = subprocess.run([engine, "--traits-dir", str(ROOT), "--format", "json",
                          *map(str, paths)], check=True, text=True,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if "Failed to load traits" in run.stderr or "skipped" in run.stderr.lower():
        raise AssertionError(run.stderr)
    reports = []
    decoder = json.JSONDecoder()
    rest = run.stdout
    while rest.strip():
        obj, end = decoder.raw_decode(rest.lstrip())
        rest = rest.lstrip()[end:]
        reports.extend(obj["files"])
    return {Path(f["path"]).name: {t["id"]: t for t in f.get("traits", [])}
            for f in reports}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cleave", default="cleave")
    ap.add_argument("--sample", type=Path)
    args = ap.parse_args()
    with tempfile.TemporaryDirectory(prefix="html-msmp-controls-") as tmp:
        tmp = Path(tmp)
        repeated = (ROOT / "testdata/triage-compromised-page-regression/repeated-script-inject.html").read_bytes()
        distinct = "<html><head>" + "".join(
            f'<script src="https://assets.example.invalid/lib{i}.js" async></script>\n'
            for i in range(60)) + "</head></html>"
        cases = {
            "repeated.html": repeated,
            "renamed.html": repeated.replace(b"example-cdn-a.com", b"assets.example.invalid"),
            "distinct.html": distinct.encode(),
            "comment.html": ("<html><!--" + distinct + "--></html>").encode(),
            "few.html": b'<html><script src="https://assets.example.invalid/a.js" async></script></html>',
        }
        for name, data in cases.items():
            (tmp / name).write_bytes(data)
        reports = scan(args.cleave, [tmp / n for n in cases])
        for name in cases:
            traits = reports[name]
            assert all(t["crit"] < 4 for t in traits.values()), (name, traits)
            assert (MASS in traits) == (name in {"repeated.html", "renamed.html", "distinct.html"}), name
            print("PASS", name)
        if args.sample:
            original = args.sample.read_bytes()
            # Mutations preserve the PE and all generic imports. Changing one
            # relationship must defeat the new self-delete finding.
            module = original.index(bytes.fromhex("56 8d 85 90 00 00 00 50 53 ff 15 64 c0 41 00"))
            fmt = original.index(bytes.fromhex("8d 85 90 00 00 00 50 50 57 ff 75 88 56 e8"), module)
            template_load = original.index(bytes.fromhex("bf f0 35 42 00 6b f6 03 57"), module)
            unrelated = bytearray(original)
            struct.pack_into("<I", unrelated, fmt + 2, 0x94)
            wrong_api = bytearray(original)
            struct.pack_into("<I", wrong_api, module + 11, 0x41c060)
            wrong_template = bytearray(original)
            struct.pack_into("<I", wrong_template, template_load + 1, 0x4235f1)
            renamed = original.replace(b"_vslite.bat", b"_rename.bat")
            cases = {"original.exe": original, "renamed.exe": renamed,
                     "unrelated-buffer.exe": unrelated, "wrong-api.exe": wrong_api,
                     "wrong-template.exe": wrong_template}
            for name, data in cases.items():
                (tmp / name).write_bytes(data)
            reports = scan(args.cleave, [tmp / n for n in cases])
            for name in cases:
                traits = reports[name]
                assert HOSTILE <= traits.keys(), (name, HOSTILE - traits.keys())
                assert (SELF_DELETE in traits) == (name in {"original.exe", "renamed.exe"}), name
                print("PASS", name)


if __name__ == "__main__":
    main()
