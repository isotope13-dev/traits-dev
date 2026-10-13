"""Static APK layout controls. No APK or embedded script is executed."""
import json
import os
from pathlib import Path
import struct
import subprocess
import tempfile
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PREFIX = "metadata/package/files/mobile-package::"
LAYOUTS = {PREFIX + "android-config-split-signing-layout",
           PREFIX + "android-config-split-bndtool-signature-layout"}


def code_declaration(manifest, enabled):
    """Change the typed application hasCode boolean in this binary fixture."""
    data = bytearray(manifest)
    pool = 8
    kind, header, size = struct.unpack_from("<HHI", data, pool)
    assert kind == 1
    count, _, flags, start = struct.unpack_from("<IIII", data, pool + 8)
    assert not flags & 0x100  # The fixture uses UTF-16 strings.
    strings = []
    for i in range(count):
        offset = struct.unpack_from("<I", data, pool + header + 4 * i)[0]
        at = pool + start + offset
        length = struct.unpack_from("<H", data, at)[0]
        assert length < 0x8000
        strings.append(bytes(data[at + 2:at + 2 + 2 * length]).decode("utf-16le"))
    pos = pool + size
    changed = 0
    while pos < len(data):
        kind, _, size = struct.unpack_from("<HHI", data, pos)
        assert size >= 8
        if kind == 0x102 and strings[struct.unpack_from("<I", data, pos + 20)[0]] == "application":
            start, width, count = struct.unpack_from("<HHH", data, pos + 24)
            for i in range(count):
                at = pos + 16 + start + width * i
                name = strings[struct.unpack_from("<I", data, at + 4)[0]]
                if name == "hasCode":
                    assert data[at + 15] == 0x12  # TYPE_INT_BOOLEAN
                    struct.pack_into("<I", data, at + 16, int(enabled))
                    changed += 1
        pos += size
    assert changed == 1
    return bytes(data)


def write_apk(path, members):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, value in members.items():
            archive.writestr(name, value)


def check(path, expected, expect_hostile=False):
    result = subprocess.run(
        [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT), "--format", "json", str(path)],
        capture_output=True, text=True, check=True,
        env={**os.environ, "CLEAVE_SKIP_CACHE": "1", "CLEAVE_NO_UPDATE_CHECK": "1"},
    )
    files = json.loads(result.stdout)["files"]
    traits = [t for file in files for t in file.get("traits", [])]
    ids = {t["id"] for t in traits}
    assert ids & LAYOUTS == set(expected), (path.name, "layouts", ids & LAYOUTS)
    assert bool([t for t in traits if t["crit"] == 5]) == expect_hostile, (path.name, "hostile", traits)
    if not expect_hostile:
        assert not [t for t in traits if t["crit"] >= 4], (path.name, "unexpected suspicious findings")
    print(path.name, "passed", flush=True)


with zipfile.ZipFile(HERE / "sample.apk") as archive:
    original = {i.filename: archive.read(i) for i in archive.infolist()}

with tempfile.TemporaryDirectory(prefix="android-layout-controls-") as scratch:
    scratch = Path(scratch)
    for name, mutation, expected, hostile in [
        ("renamed.vir", lambda m: None, LAYOUTS, False),
        ("declared-code.apk", lambda m: m.update({"AndroidManifest.xml": code_declaration(m["AndroidManifest.xml"], True)}), set(), False),
        ("not-config-split.apk", lambda m: m.update({"AndroidManifest.xml": m["AndroidManifest.xml"].replace("config.es".encode("utf-16le"), "normal.es".encode("utf-16le"))}), set(), False),
        # Exclusions describe member paths, independently of payload validity.
        ("dex-member.apk", lambda m: m.update({"classes.dex": b"path-presence control"}), set(), False),
        ("native-member.apk", lambda m: m.update({"lib/arm64-v8a/libworker.so": b"path-presence control"}), set(), False),
        ("shadow-manifest.apk", lambda m: m.update({"AndroidManifest.xml": code_declaration(m["AndroidManifest.xml"], True), "assets/AndroidManifest.xml": m["AndroidManifest.xml"]}), set(), False),
        # A manifest declaration must never suppress an actual attack finding.
        ("concealed-script.apk", lambda m: m.update({"assets/network.js": (ROOT / "testdata/reverse-shell/revshell.js").read_bytes()}), LAYOUTS, True),
    ]:
        members = dict(original)
        mutation(members)
        path = scratch / name
        write_apk(path, members)
        check(path, expected, hostile)
print("7 Android layout regression controls passed")
