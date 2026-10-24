#!/usr/bin/env python3
"""Check comment boundaries, relocated consumers and invalid CIL tokens."""
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

here = Path(__file__).resolve().parent
root = here.parents[2]
scratch = Path(sys.argv[1]).resolve()
scratch.mkdir(parents=True, exist_ok=True)
for name in (
    "hidden-agent-pipeline.md", "split-comment-and-command.md",
    "ordinary-installation.md", "phrase-only.md", "comment-only.html",
    "invalid-call-traps.dll",
):
    shutil.copyfile(here / name, scratch / name)

# A nearby control changes only the invalid token table byte. Keep the
# skipped call and null-array trap instructions to test the actual distinction.
data = (here / "invalid-call-traps.dll").read_bytes()
pattern = re.compile(re.escape(bytes.fromhex("2B 09 28")) + b"..."
                     + b"[\x30-\x6f]"
                     + re.escape(bytes.fromhex("14 16 9A 26 16 2D F9")), re.S)
assert len(pattern.findall(data)) >= 3
valid = pattern.sub(lambda m: m.group()[:6] + b"\x06" + m.group()[7:], data)
(scratch / "valid-token-control.dll").write_bytes(valid)

outside = {
    "normal-loader.exe": "testdata/benign/dotnet-normal-loader-controls.exe",
    "interop-only.exe": "testdata/benign/managed-native-interop-only.exe",
    "html-comment-control.html": "testdata/benign/triage-html-comment-control.html",
    "tirith-rules.toml": "testdata/benign/tirith-rule-docs-controls/rules.toml",
    "other-hidden-agent.html": "testdata/hostile/repository-prompt-injection/17-html-hidden-comment.html",
    "masked-native-host.ps1": "testdata/taxonomy/powershell-masked-native-host/native-host.ps1",
}
for name, source in outside.items():
    shutil.copyfile(root / source, scratch / name)

cmd = [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(root),
       "--all-files", "--format", "json", str(scratch)]
result = subprocess.run(cmd, capture_output=True, text=True, check=True)
(scratch.parent / "focused-raw.json").write_text(result.stdout)
reports = []
pending = result.stdout.lstrip()
decoder = json.JSONDecoder()
while pending:
    report, end = decoder.raw_decode(pending)
    reports.append(report)
    pending = pending[end:].lstrip()
by_name = {}
for report in reports:
    for entry in report["files"]:
        by_name.setdefault(Path(entry["path"]).name, set()).update(
            (t["id"], t["crit"]) for t in entry.get("traits", []))

prefix = "objectives/evasion/security-bypass/llm/prompt/override::"
broad = (prefix + "agent-skill-hidden-curl-pipe-instruction", 5)
comment = (prefix + "agent-skill-comment-hidden-curl-pipe", 5)
cil = ("objectives/anti-static/obfuscation/anti-decompile::cil-skipped-invalid-call-traps", 4)
opener = ("metadata/document/html::comment-opener", 1)
phrase = ("metadata/lang/natural/phrasing::secret-agent-instructions-label", 3)

assert {broad, comment} <= by_name["hidden-agent-pipeline.md"]
assert broad in by_name["split-comment-and-command.md"]
assert comment not in by_name["split-comment-and-command.md"]
assert not ({broad, comment} & by_name["ordinary-installation.md"])
assert phrase in by_name["phrase-only.md"]
assert opener in by_name["hidden-agent-pipeline.md"]
assert "comment-only.html" in by_name
assert "html-comment-control.html" in by_name
assert cil in by_name["invalid-call-traps.dll"]
for name in ("valid-token-control.dll", "normal-loader.exe", "interop-only.exe"):
    assert cil not in by_name[name], name
for name in ("tirith-rules.toml", "other-hidden-agent.html", "masked-native-host.ps1"):
    assert name in by_name

(scratch.parent / "focused-results.json").write_text(json.dumps(
    {name: sorted(rows) for name, rows in by_name.items()}, indent=2) + "\n")
print("Passed comment boundary, relocated observations and CIL controls (13 files).")
