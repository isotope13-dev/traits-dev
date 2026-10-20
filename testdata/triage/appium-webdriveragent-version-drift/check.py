#!/usr/bin/env python3
"""Controls for references misattributed by the Appium simulator build.

Compile inert string carriers and scan source; never execute the carriers.
"""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
TERM = "micro-behaviors/process/tty/terminal::terminal-type-screen"
KILL = "micro-behaviors/process/control/signal::posix-kill-function-definition"
CLANG = "micro-behaviors/process/create/shell/build::clang-invocation"
WEB = "micro-behaviors/communications/http/client/webclient::webclient-download-file"
OLD_CHECK = "metadata/package/testing/presence/path::check-test-harness-script"
IDS = {TERM, KILL, CLANG, WEB, OLD_CHECK}

with tempfile.TemporaryDirectory(prefix="appium-drift-controls-") as directory:
    base = Path(directory)
    cases = [
        ("posix.c", "typedef int pid_t; int kill(pid_t pid, int sig) { return 0; }", {KILL}),
        ("objc.m", "@implementation Session\n- (void)kill { [self.application terminate]; }\n@end", set()),
        ("other.c", "void kill(void) {}", set()),
        ("clang.sh", "#!/bin/sh\nclang -c input.c\n", {CLANG}),
        ("clang-path.sh", "#!/bin/sh\n/usr/bin/clang++ -c input.cc\n", {CLANG}),
        ("clang-directory.sh", '#!/bin/sh\nfind clang -name "*.html"\n', set()),
        ("web.ps1", "(New-Object Net.WebClient).DownloadFile($url, $path)", {WEB}),
        ("helper.js", "async function get(url, target) { await net.downloadFile(url, target); }", set()),
        ("check-dependencies.js", "module.exports = function check() {};", set()),
    ]
    paths = []
    expected = {}
    for name, contents, ids in cases:
        path = base / name
        path.write_text(contents + "\n")
        paths.append(path)
        expected[str(path)] = ids
    for name, token, ids in [("screen", "screen", set()), ("term", "TERM=screen-256color", {TERM})]:
        source = base / (name + ".c")
        binary = base / (name + ".bin")
        source.write_text('#include <stdio.h>\nint main(void) { puts(' + json.dumps(token) + '); return 0; }\n')
        subprocess.run(["cc", "-O0", str(source), "-o", str(binary)], check=True)
        paths.append(binary)
        expected[str(binary)] = ids
    result = subprocess.run(
        [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT), "--format", "json", *map(str, paths)],
        check=False, capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr
    remaining = result.stdout
    actual = {}
    decoder = json.JSONDecoder()
    while remaining.strip():
        report, end = decoder.raw_decode(remaining.lstrip())
        remaining = remaining.lstrip()[end:]
        for file in report.get("files", [report]):
            actual[file["path"]] = {t["id"] for t in file.get("traits", [])} & IDS
    for path, ids in expected.items():
        assert actual[path] == ids, (path, actual[path], ids, result.stderr)
        print(Path(path).name + ": PASS")
