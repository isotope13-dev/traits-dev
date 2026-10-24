#!/usr/bin/env python3
"""Scan inert controls from scratch paths so test-tree exclusions do not mask them."""
import argparse
import json
from pathlib import Path
import shutil
import struct
import subprocess


def class_references(values):
    pool = b""
    for value in ["ReferenceFixture", "java/lang/Object", *values, "X" * 1024]:
        data = value.encode()
        pool += b"\x01" + struct.pack(">H", len(data)) + data
    count = len(values) + 3
    pool += b"\x07\x00\x01\x07\x00\x02"
    return (b"\xca\xfe\xba\xbe" + struct.pack(">HHH", 0, 52, count + 3)
            + pool + struct.pack(">HHHHHHH", 0x21, count + 1, count + 2, 0, 0, 0, 0))


def scan(engine, rules, paths):
    result = subprocess.run([engine, "--traits-dir", str(rules), "--format", "jsonl",
                             *map(str, paths)], capture_output=True, text=True, check=True)
    reports = {}
    for line in result.stdout.splitlines():
        report = json.loads(line)
        file = report["files"][0]
        reports[Path(file["path"]).name] = {
            t["id"]: t["crit"] for t in file.get("traits", [])}
    return reports


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("scratch", type=Path)
    parser.add_argument("--cleave", default="cleave")
    parser.add_argument("--baseline", type=Path)
    parser.add_argument("--record", type=Path)
    args = parser.parse_args()
    source = Path(__file__).resolve().parent
    root = source.parents[2]
    args.scratch.mkdir(parents=True, exist_ok=True)
    paths = []
    for pattern in ("*.java", "*.php", "*.md", "*.py", "*.js", "*.xml"):
        for path in source.glob(pattern):
            if path.name in ("README.md", "check.py"):
                continue
            target = args.scratch / path.name
            shutil.copyfile(path, target)
            paths.append(target)
    for name, values in {
        "json-only.class": ["org/json/JSONObject"],
        "dpapi-json.class": ["win32/Crypt32Util", "cryptUnprotectData",
                             "GCMParameterSpec", "org/json/JSONObject"],
    }.items():
        target = args.scratch / name
        target.write_bytes(class_references(values))
        paths.append(target)
    # Keep the existing malicious pipeline and prompt-defense regressions in scope.
    paths += [root / "testdata/hostile/wp-rest-sqli-admin-shell-kit.py",
              root / "testdata/triage/great-cto-release-drift/refusal-examples.md",
              root / "testdata/triage/great-cto-release-drift/refusal-with-live-override.md",
              root / "testdata/taxonomy/password-export-and-hidden-staging/password-export.kt",
              root / "testdata/triage/apk-android-2026-10-13/sample.apk"]
    after = scan(args.cleave, root, paths)
    ids = {
        "write": "micro-behaviors/fs/write/content::php-request-selected-path-content",
        "fileshell": "objectives/command-and-control/backdoor/webshell/file-manager::php-command-request-file-read-write",
        "command": "objectives/command-and-control/backdoor/webshell/request/command::php-command-webshell",
        "json": "metadata/import/framework::jvm-org-json-object-reference",
        "decrypt": "objectives/credential-access/discord/token::java-class-dpapi-gcm-token-decryptor",
        "boolean": "objectives/execution/exploit/sql-injection::boolean-sqli-context-templates",
        "union": "objectives/execution/exploit/sql-injection::union-false-predicate-template",
        "memshell": "objectives/command-and-control/backdoor/webshell/intercept/generator::java-memshell-bytecode-generator",
        "prompt": "metadata/package/documentation/agent-safety::adversarial-content-risk-discussion",
        "disclaimer": "metadata/package/documentation/security-testing::authorized-security-testing-statement",
        "chain": "objectives/execution/exploit/chain::wordpress-rest-sqli-admin-shell-chain",
        "gettext": "metadata/lang/source/syntax/call/invocation::java-kotlin-gettext-call-text",
        "message": "micro-behaviors/communications/ipc/message::postmessage-json-stringify",
        "flutter": "micro-behaviors/process/interpreter/webview::flutter-webview-js-channel-bridge",
        "boot": "metadata/permission/activation::android-boot-completed-permission-reference",
    }
    assertions = []

    def expect(name, present=(), absent=()):
        traits = after[name]
        for key in present:
            assert ids[key] in traits, (name, "missing", ids[key])
        for key in absent:
            assert ids[key] not in traits, (name, "unexpected", ids[key])
        assertions.append(name)

    expect("json-only.class", ["json"], ["decrypt"])
    expect("dpapi-json.class", ["json", "decrypt"])
    expect("request-shell.php", ["write", "fileshell", "command"])
    expect("file-editor.php", ["write"], ["fileshell", "command"])
    expect("fixed-path.php", absent=["write", "fileshell"])
    expect("ordinary-query.py", absent=["boolean", "union"])
    expect("boolean-probes.py", ["boolean", "union"])
    expect("shell-generator.java", ["memshell"])
    expect("notification.java", ["gettext"], ["memshell"])
    expect("service-worker.js", ["message"], ["flutter"])
    expect("flutter.js", ["message", "flutter"])
    expect("AndroidManifest.xml", ["boot"])
    expect("disclaimer.md", ["disclaimer"])
    assert not any("industrialxpl" in x for x in after["disclaimer.md"])
    expect("prompt-risk.md", ["prompt"])
    expect("sql-risk.md", absent=["prompt"])
    expect("wp-rest-sqli-admin-shell-kit.py", ["chain"])
    before = scan(args.cleave, args.baseline, paths) if args.baseline else None
    if before:
        # Relabeling and added coverage must retain these established attack findings.
        for name in ("dpapi-json.class", "request-shell.php", "shell-generator.java",
                     "wp-rest-sqli-admin-shell-kit.py", "refusal-with-live-override.md",
                     "flutter.js", "password-export.kt", "sample.apk"):
            old = {k for k, v in before[name].items() if v >= 4}
            new = {k for k, v in after[name].items() if v >= 4}
            assert old <= new, (name, "lost attack findings", sorted(old - new))
        assert after["refusal-examples.md"].get(ids["prompt"]) == before["refusal-examples.md"].get(ids["prompt"])
    if args.record:
        args.record.write_text(json.dumps({"assertions": assertions, "before": before,
                                          "after": after}, indent=2) + "\n")
    print(f"Passed {len(assertions)} controls and retained attack comparisons")


if __name__ == "__main__":
    main()
