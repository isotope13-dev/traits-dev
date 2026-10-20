"""Inert ELF controls for native Mettle identity and packaged capture coverage."""
import json
import os
from pathlib import Path
import struct
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
PREFIX = "well-known/tool/offensive/mettle::"
C2 = PREFIX + "elf-c2-command-agent"
CAPTURE = "objectives/collection/network/sniffer::mettle-sniffer-extension-capture"
NAMES = (
    "c2_register_tcp_transports",
    "tlv_dispatcher_set_session_guid",
    "sys_process_execute",
)
CERT_PARSE = "micro-behaviors/crypto/certificate/usage::mbedtls-certificate-parse-api"
KEY_PARSE = "micro-behaviors/crypto/key/import::mbedtls-private-key-parse-api"
HANDSHAKE = "micro-behaviors/communications/tls/initialize::mbedtls-handshake-api"
NEUTRAL = {CERT_PARSE, KEY_PARSE, HANDSHAKE}
SERVER_FILES = {
    "micro-behaviors/communications/socket/ssl::tls-server-certificate",
    "micro-behaviors/communications/socket/ssl::tls-server-private-key",
    "micro-behaviors/communications/socket/ssl::tls-server-certificate-key-pair",
}


def elf(table=(), rodata=(), exports=()):
    """Make a non-running ELF with named string sections, no program headers."""
    names = b"\0.text\0.strtab\0.rodata\0.shstrtab\0.dynstr\0.dynsym\0"
    dynstr = bytearray(b"\0")
    dynsym = bytearray(24)
    for name in exports:
        dynsym.extend(struct.pack("<IBBHQQ", len(dynstr), 0x12, 0, 1, 64, 1))
        dynstr.extend(name.encode() + b"\0")
    chunks = [b"\xc3", b"\0" + b"\0".join(x.encode() for x in table) + b"\0",
              b"\0".join(x.encode() for x in rodata) + b"\0", names,
              dynstr, dynsym]
    blob = bytearray(64)
    sections = [bytes(64)]
    for name, kind, flags, link, entsize, chunk in zip(
        (".text", ".strtab", ".rodata", ".shstrtab", ".dynstr", ".dynsym"),
        (1, 3, 1, 3, 3, 11), (6, 0, 2, 0, 2, 2),
        (0, 0, 0, 0, 0, 5), (0, 0, 0, 0, 0, 24), chunks,
    ):
        offset = len(blob)
        blob.extend(chunk)
        sections.append(struct.pack("<IIQQQQIIQQ", names.index(name.encode()),
                                    kind, flags, offset, offset, len(chunk),
                                    link, int(kind == 11), 1, entsize))
    shoff = len(blob)
    blob.extend(b"".join(sections))
    blob.extend(bytes(max(0, 8192 - len(blob))))
    ident = b"\x7fELF\x02\x01\x01" + bytes(9)
    blob[:64] = ident + struct.pack("<HHIQQQIHHHHHH", 3, 62, 1, 0, 0,
                                   shoff, 0, 64, 0, 0, 64, len(sections), 4)
    return bytes(blob)


capture_data = ("/build/mettle/mettle/extensions/sniffer/sniffer.c",
                "pcap_open_live", "pcap_setfilter")
cases = {
    "agent": (elf(NAMES), {C2}, {CAPTURE}),
    "bin/mettle": (elf(NAMES), {C2}, {CAPTURE}),
    "no-transport": (elf(NAMES[1:]), set(), {C2, CAPTURE}),
    "no-session": (elf((NAMES[0], NAMES[2])), set(), {C2, CAPTURE}),
    "no-command": (elf(NAMES[:2]), set(), {C2, CAPTURE}),
    "rodata-mentions": (elf(rodata=NAMES), set(), {C2, CAPTURE}),
    "capture": (elf(rodata=capture_data), {CAPTURE}, {C2}),
    "bin/sniffer": (elf(rodata=capture_data), {CAPTURE}, {C2}),
    "generic-pcap": (elf(rodata=capture_data[1:]), set(), {C2, CAPTURE}),
    "build-path-only": (elf(rodata=capture_data[:1]), set(), {C2, CAPTURE}),
    "credential-parser": (
        elf(exports=("mbedtls_x509_crt_parse", "mbedtls_pk_parse_key",
                     "mbedtls_ssl_handshake")),
        NEUTRAL, SERVER_FILES | {C2, CAPTURE},
    ),
    "parser-api-mentions": (
        elf(rodata=("mbedtls_x509_crt_parse", "mbedtls_pk_parse_key",
                    "mbedtls_ssl_handshake")),
        set(), NEUTRAL | SERVER_FILES | {C2, CAPTURE},
    ),
}
with tempfile.TemporaryDirectory(prefix="mettle-controls-", dir=ROOT) as tmp:
    paths = []
    for name, (data, _, _) in cases.items():
        path = Path(tmp) / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        paths.append(str(path))
    env = dict(os.environ, CLEAVE_TRAITS_DIR=str(ROOT), SCAN_HOPPER="")
    result = subprocess.run(
        ["atomscan", "--no-update", "--follow=none", "--mode", "slow",
         "--format", "json", *paths], env=env, text=True, capture_output=True,
    )
    assert result.returncode in (0, 1), result.stderr
    reports = [json.loads(line) for line in result.stdout.splitlines() if line]
    assert len(reports) == len(cases), result.stderr
    for report in reports:
        files = report["raw"]["files"]
        name = str(Path(files[0]["path"]).relative_to(tmp))
        traits = {t["id"]: t["crit"] for f in files for t in f.get("traits", [])}
        _, present, absent = cases[name]
        assert present <= traits.keys(), (name, "missing", present - traits.keys())
        assert not absent & traits.keys(), (name, "unexpected", absent & traits.keys())
        assert all(traits[t] == (3 if t in NEUTRAL else 5) for t in present), (name, traits)
        print("PASS", name)
