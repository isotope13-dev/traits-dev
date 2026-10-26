#!/usr/bin/env python3
"""Check saved cleave/atomscan JSONL; fixtures are analyzed, never executed."""
import argparse
import json
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("reports", nargs="+", type=Path)
args = parser.parse_args()
files = {}
for report in args.reports:
    for line in report.read_text().splitlines():
        document = json.loads(line)
        for entry in document.get("raw", document).get("files", []):
            files[Path(entry["path"]).name] = {t["id"] for t in entry.get("traits", [])}

browser = "objectives/exfiltration/stealer/browser::python-chromium-login-query-file-upload"
decrypt = "objectives/credential-access/browser/chromium::python-dpapi-chromium-login-decrypt"
upload_context = "objectives/credential-access/browser/chromium::python-dpapi-browser-query-multipart-upload"
token = "objectives/credential-access/discord/token::python-file-token-harvest-and-validation"
debug = "objectives/anti-analysis/debugger-detect/check::python-debugger-check-abort"
guest = "objectives/anti-analysis/vm-detect/process::python-guest-process-blacklist-exit"
identity = "well-known/app/infrastructure/open-vm-tools::product-marker"
persistence = "objectives/persistence/login/scheduled-task/cli::python-browser-decryptor-logon-task"
hive = "objectives/credential-access/registry::sam-system-security-hive-dump"
ntds = "objectives/credential-access/files/password-database::ntdsutil-ifm-full-dump"
cases = {
    "browser-upload.py": ({browser, decrypt, upload_context}, set()),
    "browser-unrelated-upload.py": ({decrypt, upload_context}, {browser}),
    "token-file-validation.py": ({token}, set()),
    "token-standard-validation.py": ({token}, set()),
    "token-unrelated-read.py": (set(), {token}),
    "debugger-exit.py": ({debug}, set()),
    "debugger-query.py": (set(), {debug}),
    "trace-exit.py": ({debug}, set()),
    "guest-blacklist-exit.py": ({guest}, {identity}),
    "guest-inventory.py": (set(), {guest, identity}),
    "guest-name-only.py": (set(), {guest, identity}),
    "ordinary-autorun.py": (set(), {persistence}),
    "ntds-backup.bat": ({ntds}, set()),
    "retained-hive-dump.ps1": ({hive}, set()),
    "recorded-commands.ps1": (set(), {hive}),
    "config-hive-sweep.bat": ({"objectives/credential-access/files/secret-sweep::config-secret-sweep-with-hive-dump"}, set()),
    "ntds-webroot.bat": ({ntds, "objectives/exfiltration/http/webroot-drop::web-served-credential-loot-drop"}, set()),
    "mainLoop.c": ({identity}, set()),
    "stealer.py": ({decrypt, token, persistence, debug, guest, upload_context}, {browser, identity}),
}
for name, (required, forbidden) in cases.items():
    assert name in files, f"Missing report for {name}"
    assert required <= files[name], (name, "missing", required - files[name])
    assert not forbidden & files[name], (name, "unexpected", forbidden & files[name])
print(f"Passed {len(cases)} positive, retained-coverage, and near-miss cases")
