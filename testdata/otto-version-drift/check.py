#!/usr/bin/env python3
"""Run focused controls outside testdata so fixture exclusions cannot hide errors."""
import json
import os
from pathlib import Path
import subprocess
import sys

work = Path(sys.argv[1]).resolve()
work.mkdir(parents=True, exist_ok=True)
terminal = "micro-behaviors/process/tty/terminal::"
history = "objectives/evasion/indicator-removal/history::histfile-devnull"
neutral_history = "micro-behaviors/os/env/modify::histfile-dev-null"
frame = '''def payloads(begin, command, end, ready):
    history = "export HISTFILE=/dev/null; "
    readiness = f"stty -echo 2>/dev/null; echo; echo {ready}\\n"
    framed = f'echo "{begin}"; {command}; echo "{end}$?__"\\n'
    restore = "stty echo 2>/dev/null"
    return history, readiness, framed, restore
'''
cases = {
    "framed.py": (frame, [neutral_history, terminal + "python-shell-status-frame-template"], [history]),
    "unframed.py": ('payload = "export HISTFILE=/dev/null; "\n', [history, neutral_history], []),
    "missing_restore.py": (frame.replace('    restore = "stty echo 2>/dev/null"', '    restore = ""'), [history], []),
    "commented_frame.py": ('payload = "export HISTFILE=/dev/null; "\n' + '\n'.join('# '+line for line in frame.splitlines()), [history], [terminal + "python-shell-readiness-template"]),
    "ftp_banner.py": ('is_ftp = data.startswith(b"220")\n', [], ["micro-behaviors/data/string/search::numeric-prefix-22-27-or-51-55", "objectives/credential-access/financial/credit-card/card-number::mastercard-bin--rx-3"]),
    "prefix.js": ('const matches = value.startsWith("51");\n', ["micro-behaviors/data/string/search::numeric-prefix-22-27-or-51-55"], []),
    "long_prefix.js": ('const matches = value.startsWith("220");\n', [], ["micro-behaviors/data/string/search::numeric-prefix-22-27-or-51-55"]),
    "emphasis.py": ('def credentials(login):\n    """Use *login* to select the account."""\n    return login\n', [], ["micro-behaviors/fs/path/password-store::source-credential-filename-wildcard"]),
    "wildcard.py": ('pattern = "*login*"\n', ["micro-behaviors/fs/path/password-store::source-credential-filename-wildcard"], []),
    "tool_names.py": ('tools = ("gdbserver", "strace")\n', ["micro-behaviors/process/debug/tool-markers::python-analysis-tool-name-set"], ["objectives/anti-analysis/sandbox-detect/script::python-sandbox-tool-process-set"]),
    "schema.py": ('schema = "CREATE TABLE IF NOT EXISTS sessions (id TEXT)"\n', ["micro-behaviors/data/db/schema/relational::sessions-table-sql"], ["objectives/command-and-control/infrastructure/tracking::sessions-table-sql"]),
    "helper.py": ('from transfer_utils import _run_transfer\n', ["metadata/import/package::python-transfer-helper-import"], ["objectives/command-and-control/backdoor/rat/control::python-transfer-helper-import"]),
    "transfer_method.py": ('result = self._dry_run_transfer("GET", files, dest)\n', [], ["metadata/import/package::python-transfer-helper-import"]),
    "profiles.py": ('paths = ("~/.bashrc", "~/.profile")\n', ["micro-behaviors/fs/path/config/shell::python-login-profile-targets"], ["objectives/persistence/login/shell/profile::python-login-profile-targets"]),
}
for name, (source, _, _) in cases.items():
    (work / name).write_text(source)
env = dict(os.environ)
env.pop("SCAN_HOPPER", None)
env.pop("SCAN_REGISTRY_MAP", None)
result = subprocess.run(["atomscan", "--no-update", "--mode", "slow", "--format", "json", "path", *[str(work/name) for name in cases]], env=env, text=True, capture_output=True)
(work / "scan.jsonl").write_text(result.stdout)
if result.returncode:
    raise SystemExit(result.stderr)
seen = set()
for line in result.stdout.splitlines():
    obj = json.loads(line)
    files = obj["raw"]["files"]
    name = Path(files[0]["path"]).name
    if name not in cases:
        continue
    seen.add(name)
    ids = {trait["id"] for entry in files for trait in entry.get("traits", [])}
    _, present, absent = cases[name]
    assert set(present) <= ids, (name, "missing", set(present)-ids)
    assert not set(absent) & ids, (name, "unexpected", set(absent)&ids)
    print("PASS", name)
assert seen == set(cases), ("unscanned", set(cases)-seen)
print(f"All {len(cases)} controls passed")
