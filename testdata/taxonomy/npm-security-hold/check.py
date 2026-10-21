#!/usr/bin/env python3
"""Check hostile security-holder classification, including vendored packages."""
import argparse
import copy
import io
import json
from pathlib import Path
import subprocess
import tarfile
import tempfile
import zipfile


ROOT = Path(__file__).resolve().parents[3]
MANIFEST = "objectives/supply-chain/security-hold::npm-security-holder-package"
REGISTRY = "objectives/supply-chain/security-hold::registry-security-held-package"
RULES = {MANIFEST, REGISTRY}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cleave", default=str(ROOT.parent / "cleave/target/release/cleave"))
    parser.add_argument("--sfra-vsix", type=Path, help="Also check the original SFRA VSIX")
    args = parser.parse_args()
    holder = json.loads((ROOT / "testdata/hostile/npm-security-holder-fs/package.json").read_text())
    cases = []

    with tempfile.TemporaryDirectory(prefix="npm-holder-controls-") as tmp:
        work = Path(tmp)

        def manifest_case(name, data, expected):
            path = work / name / "package.json"
            path.parent.mkdir(parents=True)
            path.write_text(json.dumps(data))
            cases.append((name, path, {MANIFEST} if expected else set()))

        # The real SFRA member has an empty description and no code. Its README
        # must not be necessary to recognize a package manifest's holder identity.
        manifest_case("sfra-fs-empty-description", holder, True)
        for name, repo in [
            ("shorthand", "npm/security-holder"),
            ("github-shorthand", "github:npm/security-holder"),
            ("bare-https-url", "https://github.com/npm/security-holder"),
            ("git-ssh-url", "git+ssh://git@github.com/npm/security-holder.git"),
            ("scp-url", "git@github.com:npm/security-holder.git"),
        ]:
            data = copy.deepcopy(holder)
            data.update(name="renamed-security-held-package", repository=repo)
            manifest_case(name, data, True)

        described = copy.deepcopy(holder)
        described["description"] = "security holding package"
        manifest_case("described-holder", described, True)

        version_only = copy.deepcopy(holder)
        version_only["repository"] = "example/ordinary-package"
        manifest_case("version-alone", version_only, False)
        repository_only = copy.deepcopy(holder)
        repository_only["version"] = "1.2.3"
        manifest_case("repository-alone", repository_only, False)
        description_only = {"name": "ordinary-package", "version": "1.2.3", "description": "security holding package"}
        manifest_case("description-alone", description_only, False)
        for name, url in [
            ("different-host", "https://example.invalid/npm/security-holder"),
            ("github-host-suffix", "https://github.com.example.invalid/npm/security-holder"),
            ("repository-suffix", "https://github.com/npm/security-holder-copy.git"),
            ("repository-query", "https://github.com/example/project?ref=npm/security-holder"),
        ]:
            data = copy.deepcopy(holder)
            data["repository"]["url"] = url
            manifest_case(name, data, False)

        readme = work / "readme-mention" / "README.md"
        readme.parent.mkdir()
        readme.write_text("# Security holding package\nDocumentation mentions 0.0.1-security and npm/security-holder.\n")
        cases.append(("readme-mention", readme, set()))

        # Registry status is classified even when no package payload is available.
        for name, fields, expected in [
            ("registry-flag", {"security_hold": True}, True),
            ("registry-description", {"description": "security holding package"}, True),
            ("registry-no-hold", {"security_hold": False}, False),
            ("registry-ordinary-deprecation", {"deprecated": "Use the next major version"}, False),
            ("registry-removed-version", {"version_removed": True}, False),
        ]:
            path = work / (name + ".registry.json")
            path.write_text(json.dumps({"ecosystem": "npm", "name": "ordinary-package", "version": "1.2.3", **fields}))
            cases.append((name, path, {REGISTRY} if expected else set()))

        carrier = {"name": "ordinary-extension", "publisher": "Example", "version": "1.0.0", "engines": {"vscode": "^1.99.0"}}

        def archive_case(name, suffix, members, expected):
            path = work / (name + suffix)
            if suffix == ".vsix":
                with zipfile.ZipFile(path, "w") as archive:
                    archive.writestr("extension/package.json", json.dumps(carrier))
                    archive.writestr("extension.vsixmanifest", '<PackageManifest Version="2.0.0"><Metadata><Identity Id="ordinary-extension" Publisher="Example" Version="1.0.0"/></Metadata></PackageManifest>')
                    for member, data in members.items():
                        archive.writestr(member, json.dumps(data))
            else:
                with tarfile.open(path, "w:gz") as archive:
                    for member, data in members.items():
                        content = json.dumps(data).encode()
                        info = tarfile.TarInfo(member)
                        info.size = len(content)
                        archive.addfile(info, io.BytesIO(content))
            cases.append((name, path, {MANIFEST} if expected else set()))

        archive_case("vendored-holder", ".vsix", {"extension/node_modules/fs/package.json": holder}, True)
        archive_case("npm-holder", ".tgz", {"package/package.json": holder}, True)
        archive_case("ordinary-carrier", ".vsix", {"extension/node_modules/ordinary/package.json": {"name": "ordinary", "version": "1.2.3"}}, False)
        archive_case("split-evidence", ".vsix", {
            "extension/node_modules/first/package.json": version_only,
            "extension/node_modules/second/package.json": repository_only,
        }, False)
        if args.sfra_vsix:
            cases.append(("original-sfra-vsix", args.sfra_vsix.resolve(), {MANIFEST}))

        result = subprocess.run(
            [args.cleave, "--traits-dir", str(ROOT), "--format", "json", *[str(p) for _, p, _ in cases]],
            cwd=ROOT, capture_output=True, text=True, timeout=300,
        )
        assert result.returncode == 0, result.stderr
        remaining = result.stdout.lstrip()
        reports = []
        while remaining:
            report, end = json.JSONDecoder().raw_decode(remaining)
            reports.append(report)
            remaining = remaining[end:].lstrip()
        assert len(reports) == len(cases), (len(reports), len(cases))
        for (name, path, expected), report in zip(cases, reports):
            files = report["files"]
            assert files and Path(files[0]["path"]) == path, (name, "wrong report")
            root = {t["id"]: t["crit"] for t in files[0].get("traits", [])}
            all_findings = {t["id"]: t["crit"] for f in files for t in f.get("traits", [])}
            assert RULES.intersection(root) == expected, (name, "root findings", root)
            assert RULES.intersection(all_findings) == expected, (name, "member findings", all_findings)
            for rule in expected:
                assert root[rule] == 5 and all_findings[rule] == 5, (name, "must be hostile")
            print(f"PASS {name}: {'hostile' if expected else 'no security-hold classification'}")
        print(f"PASS: {len(cases)} security-hold cases")


if __name__ == "__main__":
    main()
