#!/usr/bin/env python3
"""Check revision classification and archive correlation; execute no sample code."""
import io
import json
import os
from pathlib import Path
import subprocess
import tarfile
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
SOURCE = "metadata/package/dependencies/manifest/source::"
UNPINNED = SOURCE + "npm-unpinned-url-runtime-dependency"
PINNED = SOURCE + "npm-commit-pinned-github-raw-dependency"
GIST_PINNED = SOURCE + "npm-commit-pinned-gist-raw-dependency"
SINGLE = SOURCE + "npm-single-unpinned-url-runtime-dependency"
LOADER = "objectives/supply-chain/hidden-payload/remote-loader::sole-mutable-url-dependency-reexport"
PLACEHOLDER = "objectives/supply-chain/impersonation/depconf::placeholder-stub-mutable-url-source"
SHA = "0123456789abcdef0123456789abcdef01234567"


def scan(path):
    result = subprocess.run(
        [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
         "--format", "json", str(path)],
        check=True, capture_output=True, text=True,
    )
    report = json.loads(result.stdout)
    return {t["id"] for f in report["files"] for t in f.get("traits", [])}


def check(path, required=(), forbidden=()):
    traits = scan(path)
    assert set(required) <= traits, (path.name, "missing", set(required) - traits)
    assert not set(forbidden) & traits, (path.name, "unexpected", set(forbidden) & traits)
    print("PASS", path.name)


def manifest(dependencies):
    return json.dumps({"name": "example-wrapper", "version": "50.0.0",
                       "description": "Placeholder package", "dependencies": dependencies})


def archive(path, members):
    with tarfile.open(path, "w:gz") as stream:
        for name, content in members.items():
            data = content.encode()
            entry = tarfile.TarInfo("package/" + name)
            entry.size = len(data)
            stream.addfile(entry, io.BytesIO(data))


def main():
    # Real published positive, not a synthetic near miss standing in for one.
    check(HERE.parent / "suspicious/version-drift-collector-npm/survey-client-10.0.12.tgz", [UNPINNED, SINGLE, LOADER], [PINNED])
    # Verbatim npm 1.1.71 members that previously supplied the false positive.
    check(HERE.parent / "benign/version-drift-collector-npm/npm-peer-test-control.tgz", [PINNED, UNPINNED], [SINGLE, LOADER])
    with tempfile.TemporaryDirectory(prefix="url-pinning-") as temporary:
        directory = Path(temporary)
        for name, url in {
            "legacy-gist": "https://raw.github.com/gist/123/" + SHA + "/index.js",
            "legacy-gist-raw": "https://gist.github.com/raw/123/" + SHA + "/index.js",
            "modern-repo": "https://raw.githubusercontent.com/owner/repo/" + SHA + "/index.js",
            "modern-gist": "https://gist.githubusercontent.com/owner/123/raw/" + SHA + "/index.js",
        }.items():
            path = directory / (name + ".tgz")
            archive(path, {"package.json": manifest({"remote-code": url}),
                           "index.js": "module.exports = require('remote-code');"})
            pinned = GIST_PINNED if name in ("legacy-gist-raw", "modern-gist") else PINNED
            check(path, [pinned], [UNPINNED, SINGLE, LOADER, PLACEHOLDER])

        for name, url in {
            "branch": "https://raw.github.com/gist/123/main/index.js",
            "no-revision": "https://raw.github.com/gist/123/index.js",
            "custom-host-hash": "https://artifacts.example.invalid/" + SHA + "/index.js",
        }.items():
            path = directory / (name + ".tgz")
            archive(path, {"package.json": manifest({"remote-code": url}),
                           "index.js": "module.exports = require('remote-code');"})
            check(path, [UNPINNED, SINGLE, LOADER, PLACEHOLDER], [PINNED])

        path = directory / "mixed-pinned-and-mutable.tgz"
        archive(path, {"package.json": manifest({
            "fixed": "https://raw.github.com/gist/123/" + SHA + "/index.js",
            "remote-code": "https://artifacts.example.invalid/current",
        })})
        check(path, [UNPINNED, PINNED], [SINGLE, LOADER])

        path = directory / "split-manifests.tgz"
        archive(path, {
            "package.json": manifest({"fixed": "https://raw.github.com/gist/123/" + SHA + "/index.js"}),
            "other/package.json": manifest({"registry": "1.0.0", "remote-code": "https://artifacts.example.invalid/current"}),
            "index.js": "module.exports = require('remote-code');",
        })
        check(path, [UNPINNED, PINNED], [SINGLE, LOADER])


if __name__ == "__main__":
    main()
