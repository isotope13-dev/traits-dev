"""Static regression controls; generated PE entry points only return.

Never execute a specimen or a generated fixture. --before records the old
matches before rule corrections; normal mode checks the corrected claims.
"""
import argparse
import json
import lzma
from pathlib import Path
import struct
import subprocess

ROOT = Path(__file__).resolve().parents[3]
STAGE = "objectives/execution/payload/file-exec::go-zip-fetch-encoded-powershell-stage"
OLD_SYS = "micro-behaviors/os/sysinfo/process::systeminfo-token"
SYS = "micro-behaviors/os/sysinfo/profile::systeminfo-command-reference"
OLD_KRB = "micro-behaviors/os/security/auth/session::kerberos-aeskey-auth-option"
KRB = "micro-behaviors/os/security/auth/session::kerberos-aeskey-reference-context"
RUNAS = "micro-behaviors/os/privilege/elevation::runas-verb"
LEGS = {
    "micro-behaviors/communications/http/download/url::archive-url-reference-binary",
    "metadata/import/builtin::go-archive-zip-reference",
    "micro-behaviors/process/create/subprocess::go-native-exec-command-reference",
    "micro-behaviors/process/interpreter/powershell/command::encoded-command-line",
}


def pe(payload):
    header = bytearray(512)
    header[:2] = b"MZ"
    struct.pack_into("<I", header, 60, 128)
    header[128:132] = b"PE\0\0"
    struct.pack_into("<HHIIIHH", header, 132, 0x14c, 2, 0, 0, 0, 224, 0x102)
    o = 152
    struct.pack_into("<H", header, o, 0x10b)
    for off, value in ((16, 4096), (20, 4096), (24, 8192), (28, 0x400000),
                       (32, 4096), (36, 512), (56, 16384), (60, 512), (92, 16)):
        struct.pack_into("<I", header, o + off, value)
    struct.pack_into("<H", header, o + 68, 3)
    size = (len(payload) + 511) // 512 * 512
    for index, (name, va, rawsize, raw, flags) in enumerate((
        (b".text", 4096, 512, 512, 0x60000020),
        (b".rdata", 8192, size, 1024, 0x40000040),
    )):
        struct.pack_into("<8sIIIIIIHHI", header, 376 + index * 40,
                         name, rawsize, va, rawsize, raw, 0, 0, 0, 0, flags)
    return bytes(header) + b"\xc3" + bytes(511) + payload.ljust(size, b"\0")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work-dir", type=Path, required=True)
    parser.add_argument("--cleave", default="cleave")
    parser.add_argument("--before", action="store_true")
    args = parser.parse_args()
    args.work_dir.mkdir(parents=True, exist_ok=True)
    cases = []

    def case(name, data, required=(), forbidden=()):
        cases.append((name, data, set(required), set(forbidden)))

    # All four old legs match an inert PE carrying independent references.
    # The supplied real Go executable independently demonstrates the same
    # relationship error: its PowerShell template belongs to appended Beacon.
    refs = (b"archive/zip\0os/exec.Command\0https://example.org/release.zip\0"
            b"powershell -nop -EncodedCommand %s\0")
    case("independent-references.exe", pe(refs), LEGS, {STAGE})
    for value in (b"systeminfo", b"SYSTEMINFO.EXE", b"C:\\Windows\\System32\\systeminfo.exe /FO CSV"):
        case("systeminfo-" + str(len(cases)) + ".exe", pe(value), {SYS})
    for value in (b"runtime.systeminfo", b"*runtime.systeminfo", b"systeminformation", b"GetSystemInfo"):
        case("non-command-" + str(len(cases)) + ".exe", pe(value), forbidden={SYS})
    case("systeminfo-popen.py", b'import os\nos.popen("systeminfo /FO CSV").read()\n',
         {SYS, "objectives/discovery/system/fingerprint/runtime::python-win-cmd-recon"})
    case("systeminfo-command.bat", b"@echo off\nsysteminfo.exe /FO CSV\n", {
        SYS, "micro-behaviors/os/sysinfo/profile::windows-systeminfo-command"})
    case("kerberos-near.exe", pe(b"Kerberos\0aesKey\0"), {KRB})
    case("dcsync-key-auth.exe", pe(b"DRSUAPI\0kerberosLogin(aesKey=key)\0 -just-dc \0"), {
        KRB, "objectives/credential-access/dump/system::dcsync-kerberos-domain-dump"})
    case("kerberos-far.exe", pe(b"aesKey\0" + b"A" * 1024 + b"\0Kerberos\0"), forbidden={KRB})
    case("aes-only.exe", pe(b"aesKey\0TLS\0"), forbidden={KRB})
    case("runas.exe", pe(b'" -Verb runAs\0'), {RUNAS})
    case("runas-nonoption.exe", pe(b"RunAs\0"), forbidden={RUNAS})
    case("godebug-catalog.exe", pe(b"crypto/x509archive/zipskip_headers\0"),
         forbidden={"metadata/import/builtin::go-archive-zip-reference"})
    runtime = ROOT / "testdata/does-nothing/out/does-nothing-linux-386.xz"
    case("runtime-control.elf", lzma.decompress(runtime.read_bytes()),
         forbidden={"metadata/import/builtin::go-archive-zip-reference"})
    # Previously established attack controls outside this sample batch.
    existing = ROOT / "testdata/hostile/go-powershell-certutil-stager.go"
    case("retained-certutil-stage.go", existing.read_bytes(), {
        "objectives/execution/payload/file-exec::go-powershell-certutil-stage"})

    paths = []
    for name, data, _, _ in cases:
        path = args.work_dir / name
        path.write_bytes(data)
        paths.append(path)
    result = subprocess.run([args.cleave, "--traits-dir", str(ROOT), "--format", "json",
                             *map(str, paths)], check=True, capture_output=True, text=True)
    # Multiple roots can be emitted as adjacent JSON reports.
    decoder = json.JSONDecoder()
    pending = result.stdout.lstrip()
    files = []
    while pending:
        report, end = decoder.raw_decode(pending)
        files.extend(report["files"])
        pending = pending[end:].lstrip()
    by_path = {f["path"]: f for f in files}
    results = []
    for (name, _, required, forbidden), path in zip(cases, paths):
        found = {t["id"] for t in by_path[str(path)].get("traits", [])}
        if not args.before:
            assert required <= found, (name, "missing", sorted(required - found))
            assert not forbidden & found, (name, "unexpected", sorted(forbidden & found))
        results.append({"case": name, "selected": sorted(found & (required | forbidden | {OLD_SYS, OLD_KRB}))})
    (args.work_dir / "results.json").write_text(json.dumps(results, indent=2) + "\n")
    print(f"{'Recorded' if args.before else 'Passed'} {len(results)} static controls")


if __name__ == "__main__":
    main()
