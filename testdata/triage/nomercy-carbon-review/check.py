#!/usr/bin/env python3
"""Static regression checks. Never execute a specimen or generated DLL."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[3]
ETW = "objectives/evasion/anti-av/blinding::managed-etw-zero-return-byte-write-profile"
NSS = "objectives/credential-access/browser/firefox::managed-nss-login-recovery-references"
HIDE = "objectives/anti-analysis/debugger-detect/thread-hide::managed-thread-hide-class17-call-profile"
XOR = "micro-behaviors/data/encoding/xor::cil-inplace-repeating-key-byte-xor-loop"
AES = "micro-behaviors/crypto/symmetric/aes/gcm::dotnet-aes-gcm-type-name-reference"


def documents(text):
    decoder = json.JSONDecoder()
    offset = 0
    while offset < len(text):
        while offset < len(text) and text[offset].isspace():
            offset += 1
        if offset == len(text):
            return
        value, offset = decoder.raw_decode(text, offset)
        yield value


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample", type=Path, required=True)
    parser.add_argument("--scratch", type=Path, required=True)
    parser.add_argument("--cleave", default="cleave")
    args = parser.parse_args()
    original = args.sample.read_bytes()
    assert hashlib.sha256(original).hexdigest() == (
        "df9b6668f20e2c3519f73d70e7af3b00322d49b2b10fafcaeabb71306806b436"
    )
    args.scratch.mkdir(parents=True, exist_ok=True)
    patch_re = re.compile(
        rb"\x06\x1f\x33\x28...\x0a\x06\x17\x20\xc0\x00\x00\x00"
        rb"\x28...\x0a\x06\x18\x20\xc3\x00\x00\x00\x28...\x0a",
        re.S,
    )
    patch = patch_re.search(original).group()
    xor_re = re.compile(
        rb"\x06\x08\x8f...\x01\x25\x47\x07\x08\x07\x8e\x69"
        rb"\x5d\x91\x61\xd2\x52", re.S,
    )
    xor = xor_re.search(original).group()
    hide_re = re.compile(
        rb"\x1f\xfe\x73...\x0a\x1f\x11\x7e...\x0a\x16\x6f...[\x06\x0a]", re.S
    )
    hide = hide_re.search(original).group()
    variants = {
        "renamed.dll": (original, {ETW, NSS, HIDE, XOR, AES}, set()),
        "no-etw.dll": (
            original.replace("EtwEventWrite".encode("utf-16-le"), b"X\x00" * 13),
            {NSS, HIDE, XOR, AES}, {ETW},
        ),
        "no-return.dll": (
            original.replace(patch, patch[:23] + b"\x90" + patch[24:]),
            {NSS, HIDE, XOR, AES}, {ETW},
        ),
        "no-password-field.dll": (
            original.replace("encryptedPassword".encode("utf-16-le"), b"X\x00" * 17),
            {ETW, HIDE, XOR, AES}, {NSS},
        ),
        "no-xor.dll": (
            original.replace(xor, xor[:16] + b"\x58" + xor[17:]),
            {ETW, NSS, HIDE, AES}, {XOR},
        ),
        "no-aes.dll": (
            original.replace(b"AesGcm", b"NoGcmX"),
            {ETW, NSS, HIDE, XOR}, {AES},
        ),
        "class18.dll": (
            original.replace(hide, hide[:8] + b"\x12" + hide[9:]),
            {ETW, NSS, XOR, AES}, {HIDE},
        ),
    }
    expectations = {}
    for name, (data, present, absent) in variants.items():
        assert len(data) == len(original)
        path = args.scratch / name
        path.write_bytes(data)
        expectations[name] = (present, absent)
    sources = {
        "ordinary-ui.js": 'this[this.isOpen?"close":"open"](event);',
        "Callback.java": "class Callback { void onMessage(Object message) {} }",
        "Pool.java": "class Pool { Object x = Executors.newFixedThreadPool(2); }",
        "Host.java": "class Host { String name = address.getHostName(); }",
    }
    for name, source in sources.items():
        (args.scratch / name).write_text(source)
    expectations.update({
        "ordinary-ui.js": ({"metadata/lang/source/syntax/call::close-literal-near-indexed-call-text"},
                           {"micro-behaviors/process/io/stream::wsh-bracket-stdin-close-call"}),
        "Callback.java": ({"metadata/file/function::jvm-onmessage-declaration"},
                          {"micro-behaviors/communications/websocket/receive::jvm-onmessage-function"}),
        "Pool.java": ({"micro-behaviors/process/work/pool::java-fixed-thread-pool-source"},
                      {"micro-behaviors/process/create/workers::java-fixed-thread-pool-source"}),
        "Host.java": ({"micro-behaviors/os/sysinfo/hostname::source-hostname-helper-call"},
                      {"micro-behaviors/communications/icmp/channel::source-icmp-host-identity"}),
    })
    run = subprocess.run([
        args.cleave, "--traits-dir", str(ROOT), "--disable", "radare2",
        "--format", "json", str(args.scratch),
    ], text=True, capture_output=True, check=True)
    (args.scratch / "analysis.jsonl").write_text(run.stdout)
    checked = []
    for report in documents(run.stdout):
        for file in report["files"]:
            name = Path(file["path"]).name
            if name not in expectations:
                continue
            traits = {t["id"] for t in file.get("traits", [])}
            present, absent = expectations[name]
            assert present <= traits, (name, "missing", present - traits)
            assert not absent & traits, (name, "unexpected", absent & traits)
            if name.endswith(".dll"):
                # These four profiles use strings/metadata. The fifth theft
                # finding needs Rizin's ExecuteReader symbol projection and
                # is checked by the complete atomscan before/after comparison.
                required_theft = {
                    "objectives/credential-access/browser/app-bound::app-bound-key-remote-injection-apis",
                    "objectives/credential-access/browser/chromium::managed-chromium-login-appbound-extraction",
                    "objectives/exfiltration/stealer/browser::managed-chromium-appbound-http-export",
                    "objectives/exfiltration/stealer/token::managed-messaging-app-session-archive-upload",
                }
                assert required_theft <= traits, (name, required_theft - traits)
            else:
                assert not [t for t in file.get("traits", []) if t["crit"] >= 4], name
            checked.append(name)
    assert set(checked) == set(expectations), (set(expectations) - set(checked))
    print(f"Passed {len(checked)} positive, mutation and source controls")


if __name__ == "__main__":
    main()
