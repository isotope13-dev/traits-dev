"""Generate static controls from the reviewed PE; never execute the sample.

Usage: python3 controls.py ORIGINAL_PE SCRATCH_DIRECTORY
The original supplies real imports and instruction paths. Mutations remove
individual observation roles; they are not replacement malware specimens.
"""
import hashlib
import json
import pathlib
import re
import sys

source, output = map(pathlib.Path, sys.argv[1:])
original = source.read_bytes()
assert hashlib.sha256(original).hexdigest() == "a9d522ef015f45256ccdc85409466338ed3bbe17dea30e035ab13cd1f38cd4c0"
output.mkdir(parents=True, exist_ok=True)
KEYS = "objectives/collection/keylog/polling::ransom-agent-polled-key-recording"
RECORD = "objectives/collection/keylog/polling::native-translated-key-recording-profile"
SURV = "objectives/collection/keylog/capture::surv-keylog-present"
WLAN = "objectives/impact/degrade/services::ransom-agent-wlan-disruption-commands"
STORE = "objectives/exfiltration/stealer/credential/record::native-telegram-session-archive-upload"
POLL = "micro-behaviors/hardware/input/keyboard/poll::polling-keyboard-api-cluster"
cases = [{"path": str(source), "present": [KEYS, RECORD, SURV, WLAN, STORE, POLL]}]


def save(name, buf, present=(), absent=()):
    p = output / (name + ".exe")
    p.write_bytes(buf)
    cases.append({"path": str(p), "present": list(present), "absent": list(absent)})


# Retain polling, foreground-window and translation imports. Replace only
# the record label recognized by the shared label atom.
buf = bytearray(original)
for m in re.finditer(rb"\[(?:ENTER|Back|Tab)\](?=[ \t\r\n]*\x00)", original, re.I):
    buf[m.start():m.end()] = b"~" * (m.end() - m.start())
save("polling-without-record-labels", buf, [POLL, WLAN, STORE], [KEYS, RECORD, SURV])

# Keep recording, but remove the independent remote ransom-control admission.
buf = bytearray(original)
a = b"start_keylogger\x00"
assert a in original
buf = buf.replace(a, b"start_keyboard\x00\x00")
assert len(buf) == len(original)
save("recording-without-keylog-task", buf, [POLL, RECORD, SURV], [KEYS, WLAN])

# Keep all tasking and keyboard evidence; remove one disruption operation.
buf = bytearray(original)
a = b"netsh wlan delete profile name=*"
assert a in original
buf = buf.replace(a, b"netsh wlan show   profile name=*")
assert len(buf) == len(original)
save("no-profile-deletion", buf, [KEYS, STORE], [WLAN])

buf = bytearray(original)
for m in re.finditer(rb'netsh interface set interface "[^"\r\n]{1,64}" disable', original):
    buf[m.end()-7:m.end()] = b"enable "
save("no-interface-disable", buf, [KEYS, STORE], [WLAN])
(output / "cases.json").write_text(json.dumps(cases, indent=2) + "\n")
