"""Static mutation controls; never executes the PE or imports npm members.

Usage: python3 controls.py ORIGINAL_PE SCRATCH_DIRECTORY
All binary controls are derived from the supplied original, not reconstructed
specimens. This file pins instruction locations for the reviewed SHA-256;
the YAML matchers themselves read variable decoder operands and use no offsets.
"""
import hashlib
import json
import pathlib
import struct
import sys

source, output = map(pathlib.Path, sys.argv[1:])
original = source.read_bytes()
assert hashlib.sha256(original).hexdigest() == "5ca11fb0605c517cc6c4943d746956dc7023f1366b1a13c83033dfb3424cf3cf"
output.mkdir(parents=True, exist_ok=True)


def offset(va):
    return va - 0x140000000 - (0xC00 if va < 0x14004B000 else 0x1200)


def keystream(seed, multiplier, index):
    state = (seed - index * multiplier) & 0xFFFFFFFF
    return (state ^ (state >> 15)) & 255


def rewrite_api(buf, va, text, seed=None, multiplier=None):
    loop = offset(va)
    seed = struct.unpack_from("<I", buf, loop + 11)[0] if seed is None else seed
    multiplier = struct.unpack_from("<I", buf, loop + 3)[0] if multiplier is None else multiplier
    struct.pack_into("<I", buf, loop + 11, seed)
    struct.pack_into("<I", buf, loop + 3, multiplier)
    base = buf[loop + 28]
    for j, byte in enumerate(text):
        size = 4 if j < 12 else 2
        prefix = b"\xc7\x44\x24" if size == 4 else b"\x66\xc7\x44\x24"
        displacement = base + (j // 4) * 4 if j < 12 else base + 12
        pos = buf.rfind(prefix + bytes([displacement]), loop - 128, loop)
        assert pos >= 0
        buf[pos + len(prefix) + 1 + (j % 4 if j < 12 else j - 12)] = byte ^ keystream(seed, multiplier, j)


def rewrite_run(buf, text, seed=None, multiplier=None):
    init, loop = offset(0x1400167E9), offset(0x140016880)
    seed = struct.unpack_from("<I", buf, loop + 11)[0] if seed is None else seed
    multiplier = struct.unpack_from("<I", buf, loop + 6)[0] if multiplier is None else multiplier
    struct.pack_into("<I", buf, loop + 11, seed)
    struct.pack_into("<I", buf, loop + 6, multiplier)
    for j, byte in enumerate(text):
        if j < 16:
            dest = offset(0x14005A5E0) + j
        elif j < 32:
            dest = offset(0x14005A650) + j - 16
        elif j < 44:
            dest = init + 29 + ((j - 32) // 4) * 7 + (j - 32) % 4
        else:
            dest = init + 51
        buf[dest] = byte ^ keystream(seed, multiplier, j)


AMSI = "micro-behaviors/os/security/amsi::index-mixed-xor-scan-buffer-name"
ETW = "micro-behaviors/os/telemetry/logging/event::index-mixed-xor-event-write-name"
RUN = "micro-behaviors/os/registry/keys/autostart::index-mixed-xor-run-key-path"
APATCH = "objectives/evasion/anti-av/amsi::index-xor-amsi-invalidarg-patch"
EPATCH = "objectives/evasion/anti-av/blinding::index-xor-etw-zero-return-patch"
PERSIST = "objectives/persistence/login/registry/run-key::extortion-concealed-run-key-self-copy"
RANSOM = "objectives/impact/ransom/encrypt/bulk-encryption::bcrypt-file-encryption-payment-demand"
C2 = "objectives/command-and-control/remote-command/tasking::discord-extortion-shell-tasking"
SCREEN = "objectives/exfiltration/stealer/screen::discord-extortion-screen-upload"
FILE_UPLOAD = "objectives/exfiltration/stealer/file::discord-extortion-file-upload-task"
GATES = "objectives/anti-analysis/sandbox-detect/timing::x64-uptime-cpu-shared-abort"
run_path = b"Software\\Microsoft\\Windows\\CurrentVersion\\Run"
cases = []


def save(name, buf, present=(), absent=()):
    path = output / (name + ".exe")
    path.write_bytes(buf)
    cases.append({"path": str(path), "present": list(present), "absent": list(absent)})


buf = bytearray(original)
rewrite_api(buf, 0x140017CA0, b"AmsiScanBuffer", 0x10203040, 0x91735A21)
rewrite_api(buf, 0x140017EB0, b"EtwEventWrite", 0x87654321, 0x31415927)
rewrite_run(buf, run_path, 0x13572468, 0xA01927D3)
save("different-seeds-and-multipliers", buf, [AMSI, ETW, RUN, APATCH, EPATCH, PERSIST])

for va, text, atom, composite, name in [
    (0x140017CA0, b"AmsiScanBuffex", AMSI, APATCH, "different-amsi-target"),
    (0x140017EB0, b"EtwEventWritx", ETW, EPATCH, "different-etw-target"),
]:
    buf = bytearray(original)
    rewrite_api(buf, va, text)
    save(name, buf, absent=[atom, composite])

buf = bytearray(original)
rewrite_run(buf, run_path[:-1] + b"x")
save("different-registry-target", buf, absent=[RUN, PERSIST])

for va, atom, composite, name in [
    (0x140017DAA, AMSI, APATCH, "no-invalidarg-patch"),
    (0x140017F3B, ETW, EPATCH, "no-zero-return-patch"),
]:
    buf = bytearray(original)
    buf[offset(va)] = 0x90
    save(name, buf, [atom], [composite])

buf = bytearray(original)
start = original.index(b"payment is confirmed")
buf[start:start + len(b"payment is confirmed")] = b"payment is optional!"
save("no-payment-condition", buf, absent=[RANSOM, C2, SCREEN, PERSIST])

buf = bytearray(original)
start = original.index(b"!exec\0")
buf[start:start + 5] = b"!help"
save("no-shell-task-verb", buf, absent=[C2, SCREEN])

buf = bytearray(original)
start = original.index(b"!screen\0")
buf[start:start + 7] = b"!status"
save("no-screen-task-verb", buf, [C2], [SCREEN])

buf = bytearray(original)
start = original.index(b"!dl\0")
buf[start:start + 3] = b"!ls"
save("no-file-retrieval-task-verb", buf, [C2, SCREEN], [FILE_UPLOAD])

buf = bytearray(original)
buf[offset(0x140017099) + 14] ^= 1
save("different-resource-abort-destination", buf, absent=[GATES])
(output / "cases.json").write_text(json.dumps(cases, indent=2) + "\n")
