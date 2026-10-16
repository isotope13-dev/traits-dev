#!/usr/bin/env python3
"""Check import precision, request wording, and independent loader evidence."""
import argparse
import io
import json
from pathlib import Path
import subprocess
import tarfile
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument("--cleave", default="cleave")
args = parser.parse_args()
repo = Path(__file__).resolve().parents[3]
get_import = "metadata/import/builtin::node-http-get-named-import"
request = "micro-behaviors/communications/http/request/client::javascript-outbound-request"
version = "micro-behaviors/communications/http/url/api-path::version-manifest-url"
loader = "objectives/supply-chain/trojanized/package/loader::fresh-npm-package-obfuscator-output"
retired = {
    "objectives/supply-chain/trojanized/package/loader::obfuscated-code-reach",
    "micro-behaviors/communications/http/request/client::browser-outbound-request",
}
cases = {
    "aliased.mjs": ("import { get as retrieve } from 'node:https';\n", {get_import}, set()),
    "plain.mjs": ("import { get } from 'http';\n", {get_import}, set()),
    "typed.ts": ("import { get as retrieve, request } from 'https';\n", {get_import}, set()),
    "other-api.mjs": ("import { request as get } from 'node:https';\n", set(), {get_import}),
    "other-module.mjs": ("import { get } from 'custom-client';\n", set(), {get_import}),
    "comment.mjs": ("// import { get as retrieve } from 'node:https';\nconsole.log('documentation');\n", set(), {get_import}),
    "string.mjs": ('console.log("import { get } from \'node:https\';");\n', set(), {get_import}),
    "outbound.mjs": ("fetch('https://service.example/data');\n", {"micro-behaviors/communications/http/request/client::js-fetch-call"}, set()),
    "version.mjs": ("const update = 'https://service.example/version.txt';\n", {version}, set()),
    "ordinary-spawn.mjs": ("import { spawnSync } from 'node:child_process';\nspawnSync('node', ['app.js']);\n", {"micro-behaviors/process/create/exec::node-spawnsync-call"}, {loader}),
}
rotation = "const words = ['1']; while(!![]) { try { const n = parseInt(words[0]); words['push'](words['shift']()); break; } catch (e) {} }\n"
spawn = "require('child_process').spawnSync('node', ['app.js']);\n"
packages = {
    "new.tgz": (1, 0, 0, rotation + spawn, True),
    "burst24.tgz": (30, 3, 3, rotation + spawn, True),
    "burst48.tgz": (30, 0, 3, rotation + spawn, True),
    "old.tgz": (30, 0, 0, rotation + spawn, False),
    "no-obfuscation.tgz": (1, 0, 0, spawn, False),
    "no-capability.tgz": (1, 0, 0, rotation, False),
}

with tempfile.TemporaryDirectory(prefix="superprint-controls-") as directory:
    directory = Path(directory)
    for name, (source, _, _) in cases.items():
        (directory / name).write_text(source)
    for name, (age, releases24, releases48, source, expected) in packages.items():
        registry = {
            "ecosystem": "npm", "name": "fixture-review", "version": "1.0.0",
            "age_days": 1, "package_age_days": age,
            "releases_24h": releases24, "releases_48h": releases48,
        }
        members = {
            "package/package.json": json.dumps({"name": "fixture-review", "version": "1.0.0"}),
            "package/index.js": source,
            "package/release.registry.json": json.dumps(registry),
        }
        with tarfile.open(directory / name, "w:gz") as archive:
            for path, content in members.items():
                payload = content.encode()
                info = tarfile.TarInfo(path)
                info.size = len(payload)
                archive.addfile(info, io.BytesIO(payload))

    output = subprocess.check_output(
        [args.cleave, "--traits-dir", str(repo), "--format", "json", str(directory)],
        cwd=repo, text=True,
    )
    decoder = json.JSONDecoder()
    reports = []
    while output.strip():
        report, end = decoder.raw_decode(output.lstrip())
        reports.extend(report["files"])
        output = output.lstrip()[end:]
    for file in reports:
        assert not retired & {t["id"] for t in file.get("traits", [])}, file["path"]
    roots = {Path(f["path"]).name: f for f in reports if "!!" not in f["path"]}
    for name, (_, required, forbidden) in cases.items():
        traits = {t["id"]: t for t in roots[name].get("traits", [])}
        assert required <= traits.keys(), (name, "missing", required - traits.keys())
        assert not forbidden & traits.keys(), (name, "unexpected", forbidden & traits.keys())
        if name == "version.mjs":
            assert traits[version]["desc"] == "References an online version manifest URL"
    for name, (age, releases24, releases48, _, expected) in packages.items():
        traits = {t["id"] for t in roots[name].get("traits", [])}
        assert (loader in traits) == expected, (name, "loader", traits)
    # Current engines filter plain OR composites from emitted findings while
    # retaining them for consumers. Check the renamed helper's evaluation too.
    trace = subprocess.check_output(
        [args.cleave, "--traits-dir", str(repo), "test-rules", "--rules", request,
         str(directory / "outbound.mjs")], cwd=repo, text=True,
    )
    assert any(line.startswith(f"MATCHED {request} ") for line in trace.splitlines()), trace
print(f"PASS: {len(cases) + len(packages)} SuperPrint trait controls")
