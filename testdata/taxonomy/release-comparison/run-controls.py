#!/usr/bin/env python3
"""Check rules using neutral temporary paths, avoiding testing suppressors."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
FIXTURES = Path(__file__).resolve().parent
transport = "micro-behaviors/process/create/shell/command-string::encoded-variable-shell-command-transport"
opaque = "objectives/anti-static/obfuscation/encoding/base64::base64-d-pipe-bash"
mode = "micro-behaviors/fs/chmod/modify::shell-numeric-mode"
checks = {
    "transport.sh": ([transport], [opaque]),
    "unrelated.sh": ([opaque], [transport]),
    "reassigned.sh": ([opaque], [transport]),
    "mixed.sh": ([opaque], [transport]),
    "output-encode.sh": ([
        "micro-behaviors/data/encode/base64::command-group-base64-pipeline",
        "micro-behaviors/data/encode/base64::identity-command-base64-pipeline",
        "micro-behaviors/data/encode/base64::file-command-base64-pipeline",
    ], []),
    "expansion-encode.sh": ([], [
        "micro-behaviors/data/encode/base64::command-output-base64-pipeline",
    ]),
    "mode.sh": ([mode], ["micro-behaviors/fs/chmod/executable/mode::shell-owner-executable-numeric-mode"]),
    "executable-mode.sh": ([mode,
        "micro-behaviors/fs/chmod/executable/mode::shell-owner-executable-numeric-mode",
        ], []),
    "mode-diagnostic.sh": ([], [mode]),
    "observations.elf": ([
        "micro-behaviors/communications/socket/telnet::telnet-connection-description",
        "micro-behaviors/fs/file/attributes::file-size-limit-message",
        "micro-behaviors/fs/proc/info/path::proc-net-tcp",
        "micro-behaviors/fs/proc/info/path::proc-net-tcp-truncated-path",
    ], [
        "micro-behaviors/fs/path/app-data::chromium-preferences-file",
        "micro-behaviors/data/parse/payment::card-number-field-key-unquoted",
    ]),
    "browser-payment.elf": ([
        "micro-behaviors/fs/path/app-data::chromium-preferences-file",
        "micro-behaviors/data/parse/payment::card-number-field-key-unquoted",
    ], []),
}
with tempfile.TemporaryDirectory(prefix="release-comparison-") as tmp:
    paths = []
    for name in checks:
        paths.append(str(Path(tmp) / name))
        shutil.copyfile(FIXTURES / name, paths[-1])
    result = subprocess.run([
        os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
        "--format", "json", *paths,
    ], env={**os.environ, "CLEAVE_SKIP_CACHE": "1"}, check=True,
        text=True, capture_output=True)
    content = result.stdout.strip()
    decoder = json.JSONDecoder()
    seen = set()
    while content:
        report, end = decoder.raw_decode(content)
        content = content[end:].lstrip()
        for item in report["files"]:
            name = Path(item["path"]).name
            if name not in checks:
                continue
            seen.add(name)
            ids = {trait["id"] for trait in item.get("traits", [])}
            present, absent = checks[name]
            assert set(present) <= ids, (name, "missing", set(present) - ids)
            assert not set(absent) & ids, (name, "unexpected", set(absent) & ids)
    assert seen == set(checks), ("missing files", set(checks) - seen)
print(f"Passed {len(checks)} release-comparison controls")
