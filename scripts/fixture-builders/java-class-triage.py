#!/usr/bin/env python3
"""Build inert JVM fixtures; never executes generated classes or sample code."""
import argparse
import io
import struct
import zipfile
from pathlib import Path


def classfile(name, strings=(), imports=(), xor=False):
    pool = []

    def add(tag, data):
        pool.append(bytes([tag]) + data)
        return len(pool)

    def utf8(value):
        data = value.encode("utf-8").replace(b"\0", b"\xc0\x80")
        return add(1, struct.pack(">H", len(data)) + data)

    def cls(value):
        return add(7, struct.pack(">H", utf8(value)))

    this, parent = cls(name), cls("java/lang/Object")
    for value in strings:
        add(8, struct.pack(">H", utf8(value)))
    for owner, member, descriptor in imports:
        owner_index = cls(owner)
        member_index, descriptor_index = utf8(member), utf8(descriptor)
        signature = add(12, struct.pack(">HH", member_index, descriptor_index))
        add(10, struct.pack(">HH", owner_index, signature))
    method, descriptor, code_name = utf8("probe"), utf8("()V"), utf8("Code")
    # Allocate a char[1], XOR two integers, convert and store the character.
    code = bytes.fromhex("04 bc 05 03 04 05 82 92 55 b1") if xor else b"\xb1"
    body = struct.pack(">HHI", 4, 0, len(code)) + code + b"\0\0\0\0"
    method_info = struct.pack(">HHHHHI", 9, method, descriptor, 1, code_name, len(body)) + body
    return (bytes.fromhex("cafebabe00000034") + struct.pack(">H", len(pool) + 1)
            + b"".join(pool) + struct.pack(">HHHHHH", 0x21, this, parent, 0, 0, 1)
            + method_info + b"\0\0")


IRC = [("IRC", "sendMessage", "(Ljava/lang/String;Ljava/lang/String;)V")]
REPLACEMENT = [
    ("java/io/File", "delete", "()Z"),
    ("java/io/File", "listFiles", "()[Ljava/io/File;"),
    ("ExampleFiles", "copy", "(Ljava/lang/String;Ljava/lang/String;)V"),
]
REGISTRY = [
    ("com/ms/lang/RegKey", "setValue", "(Ljava/lang/String;Ljava/lang/String;)V"),
    ("com/ms/security/PolicyEngine", "assertPermission", "(Lcom/ms/security/PermissionID;)V"),
]
IDLE = [("com/sun/jna/platform/win32/User32", "GetLastInputInfo", "()Z")]
CHAR = [("java/lang/String", "charAt", "(I)C")]
CATALOG = ["Create a new shell for the channel", ".corrupt <file> <message>",
           ".httpflood <url> <threads> <delay>", ".udpflood <host> <threads> <delay>",
           "Haxsoft Botnet Commands"]
INFECTION = [";infectclasses", ";infectjars", ".class", ".jar", "listFiles",
             "delete", "copy", "getCanonicalPath", "download", "java/io/File", "[nBot]"]
REDIRECT = ["STARTURL", "SEARCHURL", "HOSTSURL", "CSSURL", "FAVURL",
            "Software\\Microsoft\\Internet Explorer\\Main",
            "\\system32\\drivers\\etc\\hosts", "java/io/FileOutputStream", "write"]


def fixtures():
    return [
        ("hostile", "bot-catalog", classfile("RenamedMenu", CATALOG, IRC)),
        ("hostile", "replacement-bot", classfile("RenamedSpreader", INFECTION, IRC + REPLACEMENT)),
        ("hostile", "redirector", classfile("RenamedRedirector", REDIRECT, REGISTRY)),
        ("suspicious", "rat-idle-helper", classfile("carLambo/RenamedIdle", ["A\x01B\x02C\x03D\x04EFGHIJKLM"], IDLE + CHAR, True)),
        ("suspicious", "generic-xor-decoder", classfile("ExampleDecoder", ["A\x01B\x02C\x03D\x04EFGHIJKLM"], CHAR, True)),
        ("suspicious", "catalog-without-irc", classfile("LocalMenu", CATALOG)),
        ("suspicious", "directives-without-writes", classfile("ConfigDocumentation", REDIRECT)),
        ("notable", "ordinary-idle-query", classfile("IdleTime", imports=IDLE)),
        ("notable", "ordinary-registry-write", classfile("BrowserMigration", [REDIRECT[5]], REGISTRY)),
        ("baseline", "string-only-irc-reference", classfile("Documentation", ["IRC", "sendMessage"])),
        ("notable", "ordinary-irc-send", classfile("ChatClient", imports=IRC)),
        ("notable", "car-package-only", classfile("carLambo/NamespaceOnly")),
        ("hostile", "udp-flood-sender", classfile("RenamedUDPFlood", imports=[
            ("java/net/DatagramSocket", "send", "(Ljava/net/DatagramPacket;)V")])),
        ("suspicious", "udp-flood-name-only", classfile("RenamedUDPFlood")),
        ("notable", "ordinary-datagram-sender", classfile("DatagramClient", imports=[
            ("java/net/DatagramSocket", "send", "(Ljava/net/DatagramPacket;)V")])),
    ]


def jphp_fixtures():
    def carrier(strings, imports=()):
        module = "$php_module_m" + "a" * 32
        first = classfile(module + "_class0", strings, imports)
        second = classfile(module + "_closure0", [
            "This application failed: DLL file was not found. Re-install the application"
        ])
        payload = bytes.fromhex("1c9a4a92") + first + second
        out = io.BytesIO()
        with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for name, data in [("META-INF/MANIFEST.MF", b"Manifest-Version: 1.0\r\n\r\n"),
                               ("app/application.phb", payload)]:
                archive.writestr(zipfile.ZipInfo(name, (2020, 1, 1, 0, 0, 0)), data)
        return out.getvalue()

    operands = ["java.io.tmpdir", ".exe", "getContents", "putContents", "open", "md5", "base64_encode"]
    helpers = [("php/runtime/invoke/InvokeHelper", "callStatic", "()V"),
               ("php/runtime/invoke/InvokeHelper", "call", "()V")]
    return [("hostile", "jphp-temp-exe-error", carrier(operands, helpers)),
            ("suspicious", "jphp-operands-without-invocation", carrier(operands)),
            ("notable", "jphp-error-only", carrier(["ordinary error dialog"]))]


def archive_fixtures():
    entries = ["main/threads/TerminalThread.class", "main/threads/ReadFileThread.class",
               "main/WebSocket.class", "main/threads/UpdateThread.class",
               "main/crypto/Protection.class", "org/glassfish/tyrus/client/ClientManager.class"]
    result = []
    for severity, name, paths in [("hostile", "control-archive-layout", entries),
                                   ("notable", "partial-control-layout", entries[:-1])]:
        out = io.BytesIO()
        with zipfile.ZipFile(out, "w") as archive:
            for path in paths:
                archive.writestr(zipfile.ZipInfo(path, (2020, 1, 1, 0, 0, 0)),
                                 classfile(path[:-6]))
        result.append((severity, name, out.getvalue()))
    cobalt = ["aggressor/Aggressor.class", "beacon/BeaconC2.class",
              "common/ListenerConfig.class", "aggressor/bridges/ArtifactBridge.class"]
    for severity, name, paths in [("hostile", "cobalt-control-layout", cobalt),
                                  ("notable", "partial-cobalt-layout", cobalt[:-1])]:
        out = io.BytesIO()
        with zipfile.ZipFile(out, "w") as archive:
            for path in paths:
                archive.writestr(zipfile.ZipInfo(path, (2020, 1, 1, 0, 0, 0)),
                                 classfile(path[:-6]))
        result.append((severity, name, out.getvalue()))
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2] / "testdata")
    args = parser.parse_args()
    for severity, name, data in fixtures():
        path = args.root / severity / "generated" / "java-class-triage" / (name + ".class")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        print(path)
    for severity, name, data in jphp_fixtures() + archive_fixtures():
        path = args.root / severity / "generated" / "java-class-triage" / (name + ".jar")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        print(path)
