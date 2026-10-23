#!/usr/bin/env python3
"""Static boundaries; supplied specimens are never executed.

Usage: check.py SAMPLE_ROOT SCRATCH [CLEAVE]
SCRATCH is the directory containing the independently fetched NPS control.
"""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[3]
samples, scratch = map(Path, sys.argv[1:3])
cleave = sys.argv[3] if len(sys.argv) > 3 else "cleave"
work = scratch / "controls"
work.mkdir(exist_ok=True)
elf = (samples / "4feed588acc1/sysd").read_bytes()
pe = next(p for p in (samples / "0702f413e08c").glob("2026-*")
          if p.suffix not in {".BENIGN", ".MALICIOUS"}).read_bytes()
assert hashlib.sha256(elf).hexdigest() == "4feed588acc1396e2deeb1fc04f145cfca464ba7617dc3c1c9fe7dcc545d2d1d"
assert hashlib.sha256(pe).hexdigest() == "0702f413e08c575fbfc31343e3b68e454c34ffa62a907eba9e5aa4b654240f56"

terminal = "micro-behaviors/data/control-flow/branch::x64-terminal-selector-compare"
screen = "micro-behaviors/data/control-flow/branch::x64-screen-selector-compare"
control = "objectives/command-and-control/backdoor/rat/shell::sandbox-gated-go-terminal-control"
family = "well-known/malware/backdoor/vshell::vshell-rebased-nps-implant"
aes_enc = "micro-behaviors/crypto/encrypt::aesni-block-encryption-routine"
aes_dec = "micro-behaviors/crypto/decrypt::aesni-block-decryption-routine"
deletion = "well-known/malware/rat/remcos::remcos-browser-store-deletion"
peer = "micro-behaviors/data/control-flow/branch::network-port-constant-compare"
shell = "objectives/command-and-control/backdoor/signal::source-port-triggered-shell"
cases = []


def case(name, data, matched=(), absent=()):
    p = work / name
    p.write_bytes(data)
    cases.append((p, set(matched), set(absent)))


case("agent.elf", elf, [terminal, screen, control, family, aes_enc, aes_dec])
case("without-sandbox.elf", elf.replace(b"/home/vbccsb", b"/home/normal"),
     [terminal, screen, aes_enc, aes_dec], [control, family])
case("without-terminal.elf", elf.replace(b"\x49\xb9terminal", b"\x49\xb9temporal"),
     [screen], [terminal, control, family])
case("without-screen.elf", elf.replace(b"\x81\x3ascre", b"\x81\x3aexam"),
     [terminal], [screen, control, family])
case("without-final-decrypt-round.elf", elf.replace(bytes.fromhex("66 0f 38 df c1"),
     bytes.fromhex("66 0f 38 de c1")), [aes_enc], [aes_dec])
case("without-final-encrypt-round.elf", elf.replace(bytes.fromhex("66 0f 38 dd c1"),
     bytes.fromhex("66 0f 38 dc c1")), [aes_dec], [aes_enc])
case("remcos.exe", pe, [deletion])
case("without-clearing-status.exe", pe.replace(b"found, cleared!", b"found, retained"),
     [], [deletion])

# A reconstructed tcp_wrappers-style source positive uses a real length
# pointer. This checks the technique independently of the malformed snippet.
source = b'''#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#define SPATH "/bin/sh"
#define SRUN "sh"
void service(void) {
  struct sockaddr_in from;
  socklen_t len = sizeof(from);
  if (getpeername(0, (struct sockaddr *)&from, &len) >= 0 &&
      ntohs(from.sin_port) == 421) {
    execl(SPATH, SRUN, (char *)0);
  }
}
'''
case("port-shell.c", source, [peer, shell])
case("peer-diagnostic.c", source.replace(b'execl(SPATH, SRUN, (char *)0);',
     b'(void)fd_diagnostic();'), [peer], [shell])
case("no-port-trigger.c", source.replace(b'ntohs(from.sin_port) == 421', b'1'),
     [], [peer, shell])
case("shell-path-only.c", b'#define SPATH "/bin/sh"\n',
     ["metadata/lang/source/declaration::c-shell-image-path-macro"], [shell])
case("kernel-title.c", b'int main(){prctl(15,"[kworker/0:2]",0,0,0);}\n',
     ["objectives/evasion/masquerade/process/rename::prctl-bracketed-kworker-name"])

# The official, unmodified NPS executable is a real benign near miss, not a
# synthetic substitute. Its .forage.json and original archive stay in scratch.
npc = scratch / "nps-control/unpacked/npc"
assert npc.is_file(), "Fetch official NPS v0.26.10 before running"
cases.append((npc, {"micro-behaviors/data/serialize/binary::mux-packet-pack-error"},
              {family, control, "well-known/malware/backdoor/vshell::vshell-nps-mux-pack"}))

result = subprocess.run([cleave, "--traits-dir", str(root), "--json",
                         *[str(p) for p, _, _ in cases]],
                        capture_output=True, text=True, env=os.environ.copy())
assert result.returncode == 0, result.stderr
reports = {}
for line in result.stdout.splitlines():
    for f in json.loads(line).get("files", []):
        reports[Path(f["path"]).resolve()] = {t["id"] for t in f.get("traits", [])}
failures = []
for p, expected, absent in cases:
    actual = reports[p.resolve()]
    if expected - actual or actual & absent:
        failures.append((p.name, sorted(expected - actual), sorted(actual & absent)))
assert not failures, failures
(scratch / "focused-controls.json").write_text(json.dumps({
    "cases": len(cases), "passed": True,
    "specimens_executed": False,
}, indent=2) + "\n")
print(f"PASS: {len(cases)} static controls")
