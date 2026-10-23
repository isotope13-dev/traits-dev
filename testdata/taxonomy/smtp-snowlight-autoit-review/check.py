"""Static controls. Usage: check.py TLS_C ARM64 AUTOIT OUTPUT_DIR [CLEAVE].

Optional SCITE_CONTROL and SCILEXER_CONTROL environment paths select genuine
SciTE 1.75 binaries recovered with forager from the upstream release archive.
No supplied executable, decoded stage, or mutated control is executed.
"""
import json
import os
from pathlib import Path
import subprocess
import sys

tls, arm, autoit, output = map(Path, sys.argv[1:5])
cleave = sys.argv[5] if len(sys.argv) > 5 else "cleave"
repo = Path(__file__).resolve().parents[3]
output.mkdir(parents=True, exist_ok=True)
task = "objectives/persistence/system/scheduled-task::autoit-runpe-watchdog-task-config"
run = "objectives/persistence/login/registry/run-key::autoit-runpe-run-key-config"
inject = "objectives/execution/payload/process-inject::autoit-serialized-framework-runpe"
xor = "micro-behaviors/data/encoding/xor::aarch64-bytewise-xor-loop"
stage = "objectives/execution/payload/file-exec::xor-anonymous-stage-loader"
contact = "metadata/binary/provenance/source::scintilla-author-contact"
identity = "well-known/lib/ui/scintilla::scintilla-edit-control"
cases = [(tls, {
    "objectives/command-and-control/channel/email::smtp-starttls-command-session",
    "objectives/command-and-control/remote-command/dispatch::tls-client-command-execution",
}, set()), (arm, {xor, stage}, set()),
    (autoit, {run, inject, task, contact}, {identity,
        "well-known/lib/ui/scintilla::scintilla-author-contact"})]

# A byte-transform loop is direction-neutral; removing its EOR removes that
# observation and the dependent decoded-stage claim, not unrelated findings.
data = bytearray(arm.read_bytes())
assert data[0xbec:0xbf0] == bytes.fromhex("0000154a")
data[0xbec:0xbf0] = bytes.fromhex("1f2003d5")  # ARM64 NOP
path = output / "no-xor.elf"
path.write_bytes(data)
cases.append((path, set(), {xor, stage}))

delimiter = b"@NetsealIsTheBestLicensingSystemEverCreated@"
data = autoit.read_bytes()
start = data.index(delimiter)
end = start
for _ in range(8):
    end = data.index(delimiter, end) + len(delimiter)
original = data[start:end]
fields = original.split(delimiter)
assert len(fields[4]) >= 8 and fields[5] == b"1"
for name, startup, watchdog, present, absent in [
    ("watchdog-off", fields[4], b"0", {run, inject}, {task}),
    ("hidden-startup-watchdog-off", b"2", b"0", {run, inject}, {task}),
    ("startup-and-watchdog-off", b"0", b"0", {inject}, {run, task}),
]:
    changed = fields.copy()
    changed[4], changed[5] = startup, watchdog
    serialized = delimiter.join(changed)
    # Keep every PE RVA and the following script resource intact.
    serialized += b"\0" * (len(original) - len(serialized))
    path = output / (name + ".exe")
    path.write_bytes(data[:start] + serialized + data[end:])
    cases.append((path, present, absent))

for key in ["SCITE_CONTROL", "SCILEXER_CONTROL"]:
    if key in os.environ:
        cases.append((Path(os.environ[key]), {contact, identity}, {inject, task, run}))

result = subprocess.run([cleave, "--traits-dir", str(repo), "--format", "json",
                         "--disable", "third-party", *[str(p) for p, _, _ in cases]],
                        capture_output=True, text=True, check=True)
(output / "reports.json").write_text(result.stdout)
decoder = json.JSONDecoder()
remaining = result.stdout
reports = {}
while remaining.strip():
    report, end = decoder.raw_decode(remaining.lstrip())
    remaining = remaining.lstrip()[end:]
    for file in report["files"]:
        reports[Path(file["path"]).resolve()] = {t["id"] for t in file.get("traits", [])}
for path, present, absent in cases:
    findings = reports[path.resolve()]
    assert present <= findings, (path.name, "missing", present - findings)
    assert not absent & findings, (path.name, "unexpected", absent & findings)
    print("PASS", path.name)
