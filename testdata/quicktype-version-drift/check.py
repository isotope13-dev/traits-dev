#!/usr/bin/env python3
"""Check word-list boundaries, receiver provenance and ratio placement."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
CLEAVE = sys.argv[1] if len(sys.argv) > 1 else "cleave"
WORD = "metadata/file/format/wordlist::comma-delimited-word-run"
INFLATE = "micro-behaviors/data/decompress/zlib::pako-inflate-call"
RATIO = "metadata/file/profile/string-population::js-high-encoded-string-ratio"
OLD_RATIO = "metadata/file/data-blob::js-high-encoded-string-ratio"
EXPECT = {
    "word-run.txt": ({WORD}, set()),
    "word-run-beside-array.txt": ({WORD}, set()),
    "sparse-array.txt": (set(), {WORD}),
    "boolean-array.txt": (set(), {WORD}),
    "inflate.js": ({INFLATE}, set()),
    "inflate-reference.js": (set(), {INFLATE}),
    "unrelated-inflate.js": (set(), {INFLATE}),
    "different-receiver.js": (set(), {INFLATE}),
    "inflater-and-exec.js": (
        {INFLATE, "micro-behaviors/process/interpreter/eval/direct::eval-call-text"}, set()
    ),
    "encoded-ratio.js": ({RATIO}, {OLD_RATIO}),
    "ordinary-ratio.js": (set(), {RATIO, OLD_RATIO}),
    "short-encoded-ratio.js": (set(), {RATIO, OLD_RATIO}),
}
# Name-like vocabulary must not become protocol commands or tool provenance.
SCP = "micro-behaviors/communications/ssh/transfer::scp-command-text"
IRC = "micro-behaviors/communications/irc/command::list-command-template"
CLAUDE = "micro-behaviors/process/create/agent::claude-stream-json-mode"
YACC = "metadata/build/toolchain::yacc-generation-banner"
HYPERVISOR = "micro-behaviors/os/sysinfo/virtualization::hypervisor-name-literal"
NAMESPACE = "metadata/lang/source/syntax/call/invocation::namespace-member-call-text"
PIP = "micro-behaviors/os/package-manager/install::javascript-pip-install-text"
SEED = "micro-behaviors/os/random/prng/stdlib::seed-key-math-random-assignment"
RETIRED = {
    "micro-behaviors/os/random/prng/stdlib::wallet-secret-math-random-assignment",
    "micro-behaviors/os/com/automation::namespace-method",
    "well-known/tool/development/ide-contexts::embedded-python-pip-install",
    "metadata/build/toolchain::yacc-word",
}
EXPECT.update({
    "npm-command.sh": ({"micro-behaviors/os/package-manager/install::npm-install-ignore-scripts"}, {"micro-behaviors/process/create/shell/build::npm-install-ignore-scripts"}),
    "vocabulary.js": (set(), {SCP, IRC, CLAUDE, YACC, HYPERVISOR} | RETIRED),
    "yacc-banner.c": ({YACC}, RETIRED),
    "scp-command.js": ({SCP}, set()),
    "irc-commands.js": ({IRC}, set()),
    "claude-command.js": ({CLAUDE}, set()),
    "namespace.js": ({NAMESPACE}, RETIRED),
    "shell-namespace.js": (
        {NAMESPACE, "micro-behaviors/os/com/automation::shell-namespace-copyhere"}, RETIRED
    ),
    "seed.js": ({SEED}, RETIRED),
    "pip-comment.js": ({PIP}, RETIRED),
    "hypervisor.js": ({HYPERVISOR}, set()),
    "true-array.txt": (set(), {WORD}),
})
with tempfile.TemporaryDirectory(prefix="ratio-controls-", dir=HERE) as temporary:
    generated = Path(temporary)
    for name, character, size in [
        ("encoded-ratio.js", "A", 140000),
        ("ordinary-ratio.js", "!", 140000),
        ("short-encoded-ratio.js", "A", 64000),
    ]:
        (generated / name).write_text('exports.table = "' + character * size + '";\n')
    paths = [HERE / name if (HERE / name).exists() else generated / name for name in EXPECT]
    result = subprocess.run(
        [CLEAVE, "--traits-dir", str(ROOT), "--all-files", "--format", "json", *map(str, paths)],
        text=True, capture_output=True,
    )
    if result.returncode:
        sys.exit(result.stderr or result.stdout)
    decoder = json.JSONDecoder()
    remaining = result.stdout
    seen = set()
    while remaining.strip():
        report, end = decoder.raw_decode(remaining.lstrip())
        remaining = remaining.lstrip()[end:]
        for file in report.get("files", [report]):
            name = Path(file.get("path", "")).name
            if name not in EXPECT:
                continue
            ids = {trait["id"] for trait in file.get("traits", [])}
            required, absent = EXPECT[name]
            assert required <= ids, (name, "missing", required - ids)
            assert not absent & ids, (name, "unexpected", absent & ids)
            seen.add(name)
    assert seen == set(EXPECT), ("missing files", set(EXPECT) - seen)
    print(f"PASS: {len(seen)} focused controls")
