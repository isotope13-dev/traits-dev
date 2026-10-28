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
SCREEN = "objectives/exfiltration/stealer/media::discord-extortion-screen-upload"
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
# This renames the verb; the shell handler and screenshot task remain.
save("no-shell-task-verb", buf, [C2, SCREEN, FILE_UPLOAD])

buf = bytearray(original)
start = original.index(b"!screen\0")
buf[start:start + 7] = b"!status"
# This renames the verb; it still dispatches to desktop capture.
save("no-screen-task-verb", buf, [C2, SCREEN])

buf = bytearray(original)
start = original.index(b"!dl\0")
buf[start:start + 3] = b"!ls"
# Renaming the verb leaves its file-read/upload handler reachable.
save("no-file-retrieval-task-verb", buf, [C2, SCREEN, FILE_UPLOAD])

buf = bytearray(original)
buf[offset(0x140017099) + 14] ^= 1
save("different-resource-abort-destination", buf, absent=[GATES])
# Structural file-task controls. Keep the renamed verb in every case so an
# obsolete spelling cannot satisfy the file-upload composite instead.
FILE_READ = "micro-behaviors/communications/http/request/body/file::x64-task-file-read-post-body"
renamed = bytearray(original)
pos = original.index(b"!dl\0")
renamed[pos:pos + 3] = b"!ls"

buf = bytearray(renamed)
buf[pos:pos + 3] = b"!zz"
save("file-task-renamed-again", buf, [FILE_READ, FILE_UPLOAD])

buf = bytearray(renamed)
# Redirect the task's call to the independent shell-output helper. The file
# reader and its imports remain elsewhere in the same PE.
struct.pack_into("<i", buf, offset(0x14001408C), 0x140012340 - 0x140014090)
save("file-task-unrelated-helper", buf, absent=[FILE_READ, FILE_UPLOAD])

buf = bytearray(renamed)
# Change only the API call target: ReadFile -> CreateFileW.
struct.pack_into("<i", buf, offset(0x140010C94), 0x14004B268 - 0x140010C98)
save("file-task-unrelated-read-api", buf, absent=[FILE_READ, FILE_UPLOAD])

buf = bytearray(renamed)
buf[offset(0x140010C91)] ^= 1  # ReadFile gets a different handle register.
save("file-task-different-read-handle", buf, absent=[FILE_READ, FILE_UPLOAD])

buf = bytearray(renamed)
buf[offset(0x140014049)] ^= 1  # Size and text mismatch must skip the same block.
save("file-task-unrelated-abort", buf, absent=[FILE_READ, FILE_UPLOAD])



# The file buffer must supply the constructed POST body's argument.
buf = bytearray(renamed)
buf[offset(0x140011644)] ^= 1  # RDX receives another source register.
save("file-task-unrelated-body-buffer", buf, absent=[FILE_READ, FILE_UPLOAD])

buf = bytearray(renamed)
buf[offset(0x140011AB0)] ^= 8  # Pass a different stack body to the POST helper.
save("file-task-unrelated-post-body", buf, absent=[FILE_READ, FILE_UPLOAD])

DEPLOY = "micro-behaviors/process/deploy/file-exec::x64-file-writer-success-starts-same-path"
PAYLOAD = "objectives/execution/payload/file-exec/spawn/native::extortion-task-file-write-launch"
MASQUERADE = "objectives/evasion/masquerade/version-resource/claim::unsigned-microsoft-extortion-claim"
save("retained-file-write-launch", bytearray(renamed), [DEPLOY, PAYLOAD, MASQUERADE])

buf = bytearray(renamed)
buf[offset(0x1400142F3)] ^= 8  # Start another path after the writer returns.
save("payload-different-launch-path", buf, absent=[DEPLOY, PAYLOAD])

buf = bytearray(renamed)
buf[offset(0x14001420A)] ^= 1  # Success branch no longer reaches setup/launch.
save("payload-unrelated-success-branch", buf, absent=[DEPLOY, PAYLOAD])

buf = bytearray(renamed)
struct.pack_into("<i", buf, offset(0x14001213E), 0x14004B1C8 - 0x140012142)
save("payload-reader-instead-of-writer", buf, absent=[DEPLOY, PAYLOAD])

buf = bytearray(renamed)
struct.pack_into("<i", buf, offset(0x140014334), 0x14004B2C8 - 0x140014338)
save("payload-unrelated-launch-api", buf, absent=[DEPLOY, PAYLOAD])

buf = bytearray(renamed)
old = "Microsoft Corporation".encode("utf-16le")
new = "ExampleXX Corporation".encode("utf-16le")
pos = original.index(old)
assert len(old) == len(new)
buf[pos:pos + len(old)] = new
save("extortion-without-microsoft-claim", buf, [RANSOM], [MASQUERADE])

(output / "cases.json").write_text(json.dumps(cases, indent=2) + "\n")
