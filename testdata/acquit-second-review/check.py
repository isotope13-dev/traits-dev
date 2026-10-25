#!/usr/bin/env python3
"""Focused controls for the two reviewed specimens; never executes their code."""
import argparse
import json
import os
from pathlib import Path
import subprocess


def reports(path):
    # `--format json` can concatenate root reports without newline delimiters.
    text = Path(path).read_text()
    decoder = json.JSONDecoder()
    result = []
    while text.strip():
        report, end = decoder.raw_decode(text.lstrip())
        result.append(report)
        text = text.lstrip()[end:]
    return result


def findings(path):
    return {
        f["path"]: {t["id"]: t["crit"] for t in f.get("traits", [])}
        for report in reports(path)
        for f in report.get("raw", report)["files"]
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("scratch", type=Path)
    args = parser.parse_args()
    scratch = args.scratch.resolve()
    repo = Path(__file__).resolve().parents[2]
    controls = scratch / "focused-controls"
    controls.mkdir(exist_ok=True)
    cases = {
        "stdio.zig": '''const std = @import("std");
pub fn launch() void {
    var worker = std.process.Child.init(&.{"/bin/sh", "-c", "true"}, std.heap.page_allocator);
    worker.stdout_behavior = .Ignore;
    _ = std.posix.getenv("ENABLE_FEATURE");
}
''',
        "comments.zig": '''const std = @import("std");
// worker.stdout_behavior = .Ignore;
// std.posix.getenv("ENABLE_FEATURE");
pub fn idle() void {}
''',
        "inherit.zig": '''const std = @import("std");
pub fn launch() void {
    var worker = std.process.Child.init(&.{"/bin/sh", "script.sh"}, std.heap.page_allocator);
    worker.stdout_behavior = .Inherit;
}
''',
        "shell-pair.zig": '''const argv = [_][]const u8{
    "/bin/sh", // A comment does not destroy the broader string-pair observation.
    "-c", "true",
};
''',
        "sonoma.sh": '''#!/bin/sh
kdf_domain=sn-dek-wrap-v1
payload_magic=SNP1
printf '%s\\n' "$kdf_domain" "$payload_magic"
''',
        "sonoma-body.sh": '''#!/bin/sh
kdf_domain=sn-dek-wrap-v1
payload_magic=SNP1Abcdef0123456789
printf '%s\\n' "$kdf_domain" "$payload_magic"
''',
        "enum.sh": '''#!/bin/sh
# A compiler's unrelated ELF architecture enum, not a payload envelope.
elf_machine=SNP1K
printf '%s\\n' "$elf_machine"
''',
        "header.sh": '''#!/bin/sh
curl -H 'BuildID:example' https://example.invalid/
curl -H 'BuildID: example' https://example.invalid/
''',
        "debug-type.sh": '''#!/bin/sh
# A compiler debug type, not an HTTP header.
debug_type='zig.BuildId:Payload'
printf '%s\\n' "$debug_type"
''',
    }
    for name, source in cases.items():
        (controls / name).write_text(source)
    output = scratch / "focused-after.jsonl"
    env = dict(os.environ, CLEAVE_VALIDATE="0")
    with output.open("w") as stream:
        subprocess.run(
            [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(repo),
             "--format", "json", str(controls)],
            env=env, stdout=stream, check=True,
        )
    results = {Path(p).name: ts for p, ts in findings(output).items()}
    env_read = "micro-behaviors/os/env/read::zig-posix-getenv"
    ignore = "micro-behaviors/process/fd/stdio::zig-child-stream-ignore"
    child = "micro-behaviors/process/create/subprocess::zig-child-init"
    shell_pair = "micro-behaviors/process/create/shell/command-string::zig-bin-sh-c"
    marker = "well-known/malware/stealer/sonoma::snp1-payload-magic"
    family = "well-known/malware/stealer/sonoma::pkgunpack-dek-key-exchange"
    header = "micro-behaviors/communications/http/header/custom::build-id-header"
    checks = 0
    for name, required, forbidden in [
        ("stdio.zig", [env_read, ignore, child, shell_pair], []),
        ("comments.zig", [], [env_read, ignore]),
        ("inherit.zig", [child], [ignore, shell_pair]),
        ("shell-pair.zig", [shell_pair], []),
        ("sonoma.sh", [marker, family], []),
        ("sonoma-body.sh", [marker, family], []),
        ("enum.sh", [], [marker, family]),
        ("header.sh", [header], []),
        ("debug-type.sh", [], [header]),
    ]:
        ts = results[name]
        for rule in required:
            assert rule in ts, (name, "missing", rule)
            checks += 1
        for rule in forbidden:
            assert rule not in ts, (name, "unexpected", rule)
            checks += 1
    before = findings(scratch / "controls-before.json")
    after = findings(scratch / "controls-after.json")
    moved = {
        "micro-behaviors/process/create/direct::zig-child-init": child,
        "objectives/command-and-control/dropper/staging/temp::zig-bin-sh-c": shell_pair,
    }
    random_literal = "metadata/file/profile/string-population::random-like-alphanumeric-literal-present"
    new = {env_read, ignore, random_literal}
    for path, old_traits in before.items():
        expected = {moved.get(rule, rule): crit for rule, crit in old_traits.items()}
        actual = {rule: crit for rule, crit in after[path].items() if rule not in new}
        if random_literal in after[path] and random_literal not in old_traits:
            # The existing env-read directory consumer now evaluates this
            # dependency. Its incomplete literal observation is preserved.
            assert env_read in after[path] and after[path][random_literal] == 1
            checks += 1
        assert expected == actual, (
            path, "lost", set(expected) - set(actual), "gained", set(actual) - set(expected)
        )
        checks += 1
    budget_before = findings(scratch / "budget-before.json")
    budget_after = findings(scratch / "budget-after.json")
    argv = "metadata/lang/source/syntax/command::python-interpreter-file-argv-fragment"
    console = "micro-behaviors/os/console/io::powershell-console-writeline"
    budget_moves = {
        "micro-behaviors/process/create/subprocess::python-interpreter-file-argument": argv,
        "micro-behaviors/process/fd/stdio::powershell-console-writeline": console,
    }
    for path, old_traits in budget_before.items():
        expected = {budget_moves.get(rule, rule): crit for rule, crit in old_traits.items()}
        assert expected == budget_after[path], path
        checks += 1
    budget_results = {Path(path).name: ts for path, ts in budget_after.items()}
    for name, rule, present in [
        ("argv-only.py", argv, True),
        ("mcp-exec.py", argv, True),
        ("other-program.py", argv, False),
        ("local-chunks.ps1", console, True),
        ("query-output.py", console, True),
        ("query-output.sql", console, True),
        ("other-method.ps1", console, False),
    ]:
        assert (rule in budget_results[name]) == present, (name, rule)
        checks += 1
    print(f"Passed {checks} assertions across {len(results)} focused controls and {len(before)} existing analysis units")


if __name__ == "__main__":
    main()
