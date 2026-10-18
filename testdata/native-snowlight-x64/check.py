"""Static regression controls; never execute the supplied ELF specimen.

Usage: python3 check.py SAMPLE OUTPUT_DIR [CLEAVE]
The output directory holds altered, nonexecuted copies and the scan report.
"""
import json
import pathlib
import subprocess
import sys

sample, output = map(pathlib.Path, sys.argv[1:3])
cleave = sys.argv[3] if len(sys.argv) > 3 else "cleave"
output.mkdir(parents=True, exist_ok=True)
original = sample.read_bytes()
memfd = "micro-behaviors/mem/anonymous/create::memfd-create-syscall-number-x64"
xor = "micro-behaviors/data/decode/xor::elf-bytewise-xor-loop"
profile = "micro-behaviors/process/create/exec::socket-anonymous-exec-api-profile"
payload = "objectives/execution/payload/file-exec::xor-anonymous-stage-loader"
tcp = "objectives/execution/payload/file-exec::linux-fexecve-tcp-downloader"
mask = "objectives/evasion/masquerade/process/system-name::kworker-masqueraded-anonymous-stage"
full = {memfd, xor, profile, payload, tcp, mask}
cases = []


def case(name, old=None, new=None, present=full, absent=()):
    data = original
    if old is not None:
        assert len(old) == len(new) and data.count(old) == 1, name
        data = data.replace(old, new)
    path = output / (name + ".elf")
    path.write_bytes(data)
    cases.append((path, set(present), set(absent)))


case("original")
case("different-xor-key", bytes.fromhex("80 30 99 48 FF C0"),
     bytes.fromhex("80 30 51 48 FF C0"))
case("different-endpoint", b"124.222.150.13", b"111.111.111.11")
case("missing-xor-back-edge", bytes.fromhex("39 CE 7C F2"),
     bytes.fromhex("39 CE 90 90"), present={memfd, profile, mask},
     absent={xor, payload, tcp})
case("zero-xor-key", bytes.fromhex("80 30 99 48 FF C0"),
     bytes.fromhex("80 30 00 48 FF C0"), present={memfd, profile, mask},
     absent={xor, payload, tcp})
case("different-syscall", bytes.fromhex("BF 3F 01 00 00 E8"),
     bytes.fromhex("BF 3E 01 00 00 E8"), present={xor},
     absent={memfd, profile, payload, tcp, mask})
case("missing-receive", b"recv\0", b"rxyz\0", present={memfd, xor},
     absent={profile, payload, tcp, mask})
case("missing-fexecve", b"fexecve\0", b"fzzzzzz\0", present={memfd, xor},
     absent={profile, payload, tcp, mask})
case("missing-syscall-wrapper", b"syscall\0", b"szzzzzz\0", present={xor},
     absent={memfd, profile, payload, tcp, mask})

repo = pathlib.Path(__file__).resolve().parents[2]
result = subprocess.run([cleave, "--traits-dir", str(repo), "--format", "json",
                         "--disable", "third-party", *[str(p) for p, _, _ in cases]],
                        text=True, capture_output=True, check=True)
(output / "reports.json").write_text(result.stdout)
decoder = json.JSONDecoder()
remaining = result.stdout
reports = {}
while remaining.strip():
    report, end = decoder.raw_decode(remaining.lstrip())
    remaining = remaining.lstrip()[end:]
    for file in report["files"]:
        reports[pathlib.Path(file["path"]).name] = {
            t["id"] for t in file["traits"]}
for path, present, absent in cases:
    findings = reports[path.name]
    assert present <= findings, (path.name, "missing", present - findings)
    assert not absent & findings, (path.name, "unexpected", absent & findings)
    print("PASS", path.stem)
