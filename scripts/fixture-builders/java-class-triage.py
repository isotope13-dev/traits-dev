#!/usr/bin/env python3
"""Build inert JVM fixtures; never executes generated classes or sample code."""
import argparse
import io
import struct
import zipfile
from pathlib import Path


def classfile(name, strings=(), imports=(), xor=False, native_methods=(), interfaces=(),
              superclass="java/lang/Object", access_flags=0x21):
    pool = []

    def add(tag, data):
        pool.append(bytes([tag]) + data)
        return len(pool)

    def utf8(value):
        data = value.encode("utf-8").replace(b"\0", b"\xc0\x80")
        return add(1, struct.pack(">H", len(data)) + data)

    def cls(value):
        return add(7, struct.pack(">H", utf8(value)))

    this, parent = cls(name), cls(superclass)
    interface_indices = [cls(name) for name in interfaces]
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
    native_info = b"".join(struct.pack(">HHHH", 0x109, utf8(name), descriptor, 0)
                           for name in native_methods)
    return (bytes.fromhex("cafebabe00000034") + struct.pack(">H", len(pool) + 1)
            + b"".join(pool) + struct.pack(">HHHH", access_flags, this, parent, len(interfaces))
            + b"".join(struct.pack(">H", index) for index in interface_indices)
            + struct.pack(">HH", 0, 1 + len(native_methods))
            + method_info + native_info + b"\0\0")


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
        ("hostile", "declared-secret-theft", classfile("RenamedCollector", native_methods=[
            "steal_cookies", "extractAndWritePasswords"])),
        ("hostile", "renamed-theft-methods", classfile("OtherCollector", native_methods=[
            "stealCookies", "extract_and_write_passwords"])),
        ("suspicious", "quoted-theft-methods", classfile("MethodDocumentation", strings=[
            "steal_cookies", "extractAndWritePasswords"])),
        ("suspicious", "imported-theft-methods", classfile("ReferenceOnly", imports=[
            ("OtherClass", "steal_cookies", "()V"),
            ("OtherClass", "extractAndWritePasswords", "()V")])),
        ("suspicious", "cookie-theft-method-only", classfile("PartialCollector", native_methods=[
            "steal_cookies"])),
        ("baseline", "ordinary-native-binding", classfile("NativeBindings", native_methods=[
            "getCookie", "setCookie"])),
        ("notable", "allatori-marker-only", classfile("DemoProtected", strings=["AllatorixDemo"])),
        ("suspicious", "allatori-control-table", classfile("DemoProtected", strings=[
            "AllatorixDemo", "A\x01B\x02C\x03D\x04EFGHIJKLM"])),
        ("suspicious", "command-prompt-listener", classfile("CommandPromptServer", imports=[
            ("java/net/ServerSocket", "accept", "()Ljava/net/Socket;"),
            ("ClientProcessor", "<init>", "()V")])),
        ("notable", "ordinary-client-listener", classfile("OrdinaryServer", imports=[
            ("java/net/ServerSocket", "accept", "()Ljava/net/Socket;"),
            ("ClientProcessor", "<init>", "()V")])),
        ("notable", "command-server-role-without-listener", classfile("CommandPromptServer")),
        ("notable", "keylogging-documentation", classfile("Documentation", strings=[
            "keylogger integration documentation"])),
        ("hostile", "global-keylogger-buffer", classfile("RenamedRecorder", native_methods=[
            "getKeylogs"], interfaces=["org/jnativehook/keyboard/NativeKeyListener"], imports=[
            ("org/jnativehook/GlobalScreen", "registerNativeHook", "()V"),
            ("org/jnativehook/keyboard/NativeKeyEvent", "getKeyText", "(I)Ljava/lang/String;")])),
        ("notable", "ordinary-global-hotkey", classfile("HotkeyManager",
            interfaces=["org/jnativehook/keyboard/NativeKeyListener"], imports=[
            ("org/jnativehook/GlobalScreen", "registerNativeHook", "()V"),
            ("org/jnativehook/keyboard/NativeKeyEvent", "getKeyText", "(I)Ljava/lang/String;")])),
        ("hostile", "reflected-live-keylogger", classfile("RenamedKeylogger",
            strings=["keyCode", "keyText"], native_methods=["disableJNHLogger"], imports=[
            ("java/lang/reflect/Proxy", "newProxyInstance", "()V"),
            ("RemoteClient", "sendPacket", "()V")])),
        ("suspicious", "reflected-input-without-keylog-role", classfile("RemoteInput",
            strings=["keyCode", "keyText"], native_methods=["disableJNHLogger"], imports=[
            ("java/lang/reflect/Proxy", "newProxyInstance", "()V"),
            ("RemoteClient", "sendPacket", "()V")])),
        ("suspicious", "quoted-reflected-keylog-pattern", classfile("Documentation",
            strings=["keyCode", "keyText", "disableJNHLogger", "newProxyInstance", "sendPacket"])),
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


def endpoint_fixtures():
    browser = classfile("example/RenamedCollector", native_methods=[
        "steal_cookies", "extractAndWritePasswords"])
    discord = classfile("example/RenamedTokens", native_methods=[
        "getDiscordToken", "CheckDiscordToken", "DecryptData", "ReadFile"])
    telegram = classfile("example/RenamedBackup", native_methods=[
        "copyTelegramData", "GetTelegramAppdata", "copyDirectoryRecursively"])
    result = []
    for severity, name, modules in [
            ("hostile", "padded-native-theft-bundle", [browser, discord, telegram]),
            ("suspicious", "token-helper-without-theft-bundle", [discord]),
            ("suspicious", "backup-without-theft-bundle", [telegram])]:
        out = io.BytesIO()
        with zipfile.ZipFile(out, "w") as archive:
            for i, data in enumerate(modules):
                archive.writestr(zipfile.ZipInfo(f"example/Module{i}.class", (2020, 1, 1, 0, 0, 0)),
                                 data, compress_type=zipfile.ZIP_DEFLATED)
            # Larger, uninteresting classes must not hide the small native
            # declarations below the archive's bounded class sample.
            for i in range(40):
                data = classfile(f"padding/Class{i}", strings=["ordinary padding" * 100])
                archive.writestr(zipfile.ZipInfo(f"padding/Class{i}.class", (2020, 1, 1, 0, 0, 0)),
                                 data, compress_type=zipfile.ZIP_DEFLATED)
        result.append((severity, name, out.getvalue()))
    return result


def keylogger_fixtures():
    reporter = classfile("example/Capture", strings=["drainQueue"],
                        native_methods=["startKeyloggerLoop"], imports=[
        ("net/dv8tion/jda/api/entities/channel/middleman/MessageChannel", "sendMessage", "()V")])
    hook = classfile("example/Capture$Hook", imports=[
        ("example/WindowsAPI", "SetWindowsHookExW", "()V"),
        ("example/WindowsAPI", "ToUnicode", "()V")])
    control = classfile("example/KeyControl", native_methods=["startKeylogger", "stopKeylogger"], imports=[
        ("example/CLS_JNIKeylog", "<init>", "()V"),
        ("java/net/Socket", "getInputStream", "()Ljava/io/InputStream;"),
        ("java/net/Socket", "getOutputStream", "()Ljava/io/OutputStream;")])
    reader = classfile("example/KeyControl$Reader", imports=[
        ("example/CLS_JNIKeylog", "getChar", "()Ljava/lang/String;")])
    result = []
    for severity, name, members in [
        ("hostile", "nested-keylogger-reporting", [("example/Capture.class", reporter),
                                                   ("example/Capture$Hook.class", hook)]),
        ("suspicious", "unrelated-hook-and-reporter", [("example/Capture.class", reporter),
                                                       ("other/Unrelated.class", hook)]),
        ("hostile", "native-keylog-socket-control", [("example/KeyControl.class", control),
                                                     ("example/KeyControl$Reader.class", reader)])]:
        out = io.BytesIO()
        with zipfile.ZipFile(out, "w") as archive:
            for path, data in members:
                archive.writestr(zipfile.ZipInfo(path, (2020, 1, 1, 0, 0, 0)), data)
        result.append((severity, name, out.getvalue()))
    return result


def secret_model_fixtures():
    schemas = ["originUrl;username;password", "name;value;host;path;expiry",
               "nameOnCard;expirationMonth;expirationYear;cardNumber;cvv"]
    categories = ["PASSWORD", "COOKIE", "DISCORD", "AUTOFILL", "HISTORY", "EXTENSION"]
    result = []
    for severity, name, superclass, discord, marker, binding in [
        ("hostile", "protected-secret-collection-model", "java/lang/Record", True, True, "native"),
        ("suspicious", "protected-password-import-model", "java/lang/Record", False, True, "ordinary"),
        ("suspicious", "quoted-secret-models", "java/lang/Object", True, True, "native"),
        ("notable", "ordinary-secret-record-models", "java/lang/Record", False, False, "ordinary"),
        ("suspicious", "secret-models-without-native-binding", "java/lang/Record", True, True, "ordinary"),
        ("suspicious", "quoted-native-secret-binding", "java/lang/Record", True, True, "quoted"),
    ]:
        out = io.BytesIO()
        with zipfile.ZipFile(out, "w") as archive:
            for i, schema in enumerate(schemas):
                strings = [schema] + (["obfuscated with complexer"] if marker else [])
                data = classfile(f"renamed/Model{i}", strings=strings, superclass=superclass)
                archive.writestr(zipfile.ZipInfo(f"renamed/Model{i}.class", (2020, 1, 1, 0, 0, 0)), data)
            values = [s for s in categories if discord or s != "DISCORD"]
            data = classfile("renamed/Category", strings=values,
                             superclass="java/lang/Enum", access_flags=0x4031)
            archive.writestr(zipfile.ZipInfo("renamed/Category.class", (2020, 1, 1, 0, 0, 0)), data)
            namespace = "example" if binding == "ordinary" else "qw/chudvvick/myth/util/nss"
            data = classfile(namespace + "/NSSLibrary",
                             strings=["NSS_Init", "PK11SDR_Decrypt"] if binding == "quoted" else [],
                             native_methods=[] if binding == "quoted" else ["NSS_Init", "PK11SDR_Decrypt"])
            archive.writestr(zipfile.ZipInfo("renamed/Bindings.class", (2020, 1, 1, 0, 0, 0)), data)
        result.append((severity, name, out.getvalue()))
    return result


def webhook_fixtures():
    imports = [(owner, method, "()V") for owner, method in [
        ("com/github/kevinsawicki/http/HttpRequest", "post"),
        ("java/io/FileInputStream", "<init>"),
        ("org/apache/http/client/methods/HttpPost", "<init>"),
        ("org/apache/http/entity/mime/MultipartEntity", "addPart"),
        ("org/apache/http/entity/mime/content/InputStreamBody", "<init>")]]
    # Inert receiver ID fixtures: the suffix is deliberately a dummy token.
    fixed = "https://discordapp.com/api/webhooks/546494746021986316/inert_fixture"
    ordinary = "https://discord.com/api/webhooks/123456789012345678/inert_fixture"
    return [
        ("hostile", "reviewed-attachment-diversion", classfile("RenamedUploader",
            strings=[fixed, "webhook", "payload_json"], imports=imports)),
        ("suspicious", "ordinary-fixed-webhook-upload", classfile("AlertUploader",
            strings=[ordinary, "webhook", "payload_json"], imports=imports)),
        ("suspicious", "reviewed-receiver-without-file-upload", classfile("EndpointDocumentation",
            strings=[fixed])),
    ]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2] / "testdata")
    args = parser.parse_args()
    for severity, name, data in fixtures() + webhook_fixtures():
        path = args.root / severity / "generated" / "java-class-triage" / (name + ".class")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        print(path)
    for severity, name, data in (jphp_fixtures() + archive_fixtures() + endpoint_fixtures()
                                 + keylogger_fixtures() + secret_model_fixtures()):
        path = args.root / severity / "generated" / "java-class-triage" / (name + ".jar")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        print(path)
