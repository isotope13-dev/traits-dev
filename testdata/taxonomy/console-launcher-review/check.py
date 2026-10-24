"""Focused production-matcher controls; no generated executable is run.

Usage: python3 check.py SCRATCH_DIR
"""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location(
    "pe_controls", ROOT / "testdata/taxonomy/managed-tuner-observations/check.py")
controls = importlib.util.module_from_spec(spec)
spec.loader.exec_module(controls)

SYS = "micro-behaviors/os/sysinfo/profile::sysinfo-console-command-line"
UID = "micro-behaviors/process/identity/query::getuid-console-command-line"
CWD = "micro-behaviors/fs/directory/cwd::getlwd-console-command-line"
NET = "micro-behaviors/os/network/status::netstat"
BATCH = "well-known/tool/offensive/metasploit::meterpreter-reconnaissance-command-batch"
REDIRECT = "micro-behaviors/communications/http/redirect::dotnet-allow-auto-redirect-setter-reference"
QUERIES = {SYS, UID, CWD}


def main():
    scratch = Path(sys.argv[1])
    scratch.mkdir(parents=True, exist_ok=True)
    cases = [
        ("batch.rc", b"sysinfo\ngetuid\ngetlwd\nnetstat -atnp\nls\n",
         {*QUERIES, NET, BATCH}, {REDIRECT}),
        ("reordered.rc", b"getlwd\r\n\tgetuid \r\n  sysinfo\t\r\nnetstat -an\r\n",
         {*QUERIES, NET}, {BATCH}),
        ("local.rc", b"getlwd\n", {CWD}, {SYS, UID, NET, BATCH}),
        ("host.rc", b"sysinfo\n", {SYS}, {UID, CWD, BATCH}),
        ("identity.rc", b"getuid\n", {UID}, {SYS, CWD, BATCH}),
        ("prose.txt", b"The sysinfo command reports system properties.\n"
         b"Use getuid to query a session and getlwd for the local directory.\n",
         set(), {*QUERIES, BATCH}),
        ("functions.c", b"int sysinfo(void); int getuid(void); int getlwd(void);\n",
         set(), {*QUERIES, BATCH}),
        ("tokens.txt", b"not_sysinfo\ngetuid_suffix\ngetlwd_extra\nnetstatistic\n",
         set(), {*QUERIES, NET, BATCH}),
        # Existing script coverage must survive the additional text scope.
        ("network.sh", b"#!/bin/sh\nnetstat -an\n", {NET}, {BATCH}),
        ("policy.exe", controls.pe(b"set_AllowAutoRedirect\0"), {REDIRECT}, set()),
        ("policy-suffix.exe", controls.pe(b"set_AllowAutoRedirectExample\0"),
         set(), {REDIRECT}),
        ("policy-resource.exe", controls.pe(resource=b"set_AllowAutoRedirect\0"),
         set(), {REDIRECT}),
    ]
    for name, data, _, _ in cases:
        (scratch / name).write_bytes(data)
    result = subprocess.run([
        os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
        "--format", "json", "analyze", *[str(scratch / c[0]) for c in cases],
    ], check=True, capture_output=True, text=True)
    decoder, offset, reports = json.JSONDecoder(), 0, {}
    while offset < len(result.stdout):
        while offset < len(result.stdout) and result.stdout[offset].isspace():
            offset += 1
        if offset == len(result.stdout):
            break
        report, offset = decoder.raw_decode(result.stdout, offset)
        for f in report["files"]:
            reports[Path(f["path"]).name] = {t["id"]: t["crit"]
                                             for t in f.get("traits", [])}
    output = []
    for name, _, required, forbidden in cases:
        observed = reports[name]
        assert required <= observed.keys(), (name, required - observed.keys())
        assert not forbidden & observed.keys(), (name, forbidden & observed.keys())
        if name == "batch.rc":
            assert observed[BATCH] == 4, observed[BATCH]
        output.append({"case": name, "passed": True})
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
