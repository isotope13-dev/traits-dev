#!/usr/bin/env python3
"""Verify the corrected observations and retained objective consumers."""
import argparse
import json
import pathlib
import subprocess

BASE = pathlib.Path(__file__).resolve().parent
CASES = {
    "firewall-write.sh": (
        ["objectives/impact/degrade/firewall::alf-globalstate-disable",
         "micro-behaviors/fs/config/preferences::macos-firewall-globalstate-preference"],
        ["micro-behaviors/os/firewall/query::defaults-firewall-globalstate-read",
         "micro-behaviors/os/firewall/query::socketfilterfw-globalstate-query"],
    ),
    "firewall-query.sh": (
        ["micro-behaviors/os/firewall/query::defaults-firewall-globalstate-read",
         "micro-behaviors/os/firewall/query::socketfilterfw-globalstate-query"],
        ["objectives/impact/degrade/firewall::alf-globalstate-disable"],
    ),
    "getuid-compat.h": (
        ["metadata/file/function::getuid-zero-return-definition"],
        ["objectives/evasion/hijack-execution-flow/preload::getuid-stub-ld-preload",
         "objectives/evasion/hijack-execution-flow/preload::getuid-stub-gcc-tmp"],
    ),
    "getuid-preload.c": (
        ["objectives/evasion/hijack-execution-flow/preload::getuid-stub-ld-preload",
         "objectives/evasion/hijack-execution-flow/preload::getuid-stub-gcc-tmp"], [],
    ),
    "clone-comment.c": (
        ["metadata/lang/source/syntax/call/arguments::clone-shared-vm-call-text"],
        ["objectives/evasion/process/hidden/argv-env::clone-vm-pid-grind-source"],
    ),
    "bsd-process-info.c": (
        ["micro-behaviors/process/info/query::kern-proc-pid-reference"],
        ["objectives/evasion/kernel-hide/lkm/interface::freebsd-process-hiding"],
    ),
    "bsd-handler.c": (
        ["objectives/evasion/kernel-hide/lkm/interface::freebsd-process-hiding"], [],
    ),
    "stdio-files.c": (
        ["micro-behaviors/process/fd/stdio::startupinfo-stdio-handle-fields"],
        ["objectives/command-and-control/backdoor/bind-shell::windows-bind-shell-stdio-source"],
    ),
    "bind-shell.c": (
        ["objectives/command-and-control/backdoor/bind-shell::windows-bind-shell-stdio-source"], [],
    ),
    "adb-permissive.yml": (
        ["micro-behaviors/os/security/selinux::adb-setenforce-permissive"], [],
    ),
    "adb-enforcing.sh": (
        [], ["micro-behaviors/os/security/selinux::adb-setenforce-permissive"],
    ),
}


def documents(text):
    decoder = json.JSONDecoder(strict=False)
    while text.strip():
        text = text.lstrip()
        value, end = decoder.raw_decode(text)
        yield value
        text = text[end:]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--reports", type=pathlib.Path)
    args = parser.parse_args()
    if args.reports:
        text = args.reports.read_text()
    else:
        text = subprocess.check_output(
            ["cleave", "--traits-dir", ".", "--format", "json",
             str(BASE / "controls")], text=True,
        )
    seen = set()
    for report in documents(text):
        file = report["files"][0]
        name = pathlib.Path(file["path"]).name
        if name not in CASES:
            continue
        seen.add(name)
        ids = {trait["id"] for trait in file.get("traits", [])}
        present, absent = CASES[name]
        assert set(present) <= ids, (name, "missing", set(present) - ids)
        assert not set(absent) & ids, (name, "unexpected", set(absent) & ids)
    assert seen == CASES.keys(), ("unscanned cases", CASES.keys() - seen)
    print("11 controls passed; firewall, preload, kernel and bind-shell coverage retained")


if __name__ == "__main__":
    main()
