#!/usr/bin/env python3
"""Exercise resource variants, sparse images, and independent attack evidence."""

import io
import json
import os
from pathlib import Path
import plistlib
import struct
import subprocess
import tempfile
import zipfile


def disk_image(ignored):
    """Build a bounded UDIF image containing one raw or ignored extent."""
    sectors = 4
    fork = b"" if ignored else bytes(sectors * 512)
    table = bytearray(244)
    table[:4] = b"mish"
    struct.pack_into(">I", table, 4, 1)
    struct.pack_into(">Q", table, 16, sectors)
    struct.pack_into(">I", table, 200, 1)
    struct.pack_into(">I", table, 204, 2 if ignored else 1)
    struct.pack_into(">Q", table, 220, sectors)
    struct.pack_into(">Q", table, 236, len(fork))
    xml = plistlib.dumps({"resource-fork": {"blkx": [
        {"Name": "test partition", "Data": bytes(table)}]}})
    trailer = bytearray(512)
    trailer[:4] = b"koly"
    struct.pack_into(">I", trailer, 4, 4)
    struct.pack_into(">I", trailer, 8, 512)
    struct.pack_into(">Q", trailer, 32, len(fork))
    struct.pack_into(">Q", trailer, 216, len(fork))
    struct.pack_into(">Q", trailer, 224, len(xml))
    struct.pack_into(">Q", trailer, 492, sectors)
    return fork + xml + trailer


def main():
    repo = Path(__file__).resolve().parents[2]
    engine = os.environ.get("CLEAVE", str(repo.parent / "cleave/target/release/cleave"))
    uri = "micro-behaviors/communications/url/reference::plist-url-field"
    bookmark = "metadata/filename/identity::apple-webloc-filename"
    strings = "metadata/filename/identity::apple-localization-strings-filename"
    remote = "metadata/file/format/serialization::remote-device-class"
    resx = "metadata/file/format/managed-runtime::resx-resource-mime-declaration"
    expansion = "metadata/archive/compression::archive-high-overall-compression-expansion"
    ignored = "metadata/archive/layout::dmg-ignored-extents"
    masquerade = "objectives/evasion/masquerade/identity/bundle::generic-utils-bundle-id"
    cases = {}

    def plist_case(name, value, required=(), binary=False):
        cases[name] = (plistlib.dumps(value, fmt=plistlib.FMT_BINARY if binary else plistlib.FMT_XML),
                       set(required))

    for name, target in [("web.webloc", "https://example.invalid/report"),
                         ("local.WEBLOC", "file:///Applications/Example.app"),
                         ("script.webloc", "javascript:alert(1)"),
                         ("custom.webloc", "x:example")]:
        plist_case(name, {"URL": target}, {uri, bookmark}, binary=name.startswith("local"))
    plist_case("renamed.plist", {"URL": "https://example.invalid/report"}, {uri})
    plist_case("relative.plist", {"URL": "/report"})
    plist_case("bad-scheme.plist", {"URL": "1https:example"})
    plist_case("quoted.plist", {"description": "URL https://example.invalid"})
    plist_case("nested.plist", {"nested": {"URL": "https://example.invalid"}})
    plist_case("Localizable.strings", {"button.title": "Install"}, {strings}, binary=True)
    plist_case("Localizable.STRINGS", {"button.title": "Install"}, {strings})
    plist_case("device.plist", {"$objects": [{"$classname": "PKRemoteDevice"}]}, {remote}, binary=True)
    plist_case("device-xml.plist", {"$objects": [{"$classname": "PKRemoteDevice"}]}, {remote})
    plist_case("device-quoted.plist", {"description": "PKRemoteDevice"})
    plist_case("device-prefix.plist", {"$objects": [{"$classname": "PKRemoteDeviceHelper"}]})
    # Resource/format evidence must not suppress an independent attack indicator.
    plist_case("mixed.strings", {"CFBundleIdentifier": "com.utils.wormgpt",
                                "URL": "https://example.invalid"}, {strings, uri, masquerade})
    headers = {
        "standard.resx": '<resheader name="resmimetype"><value>text/microsoft-resx</value></resheader>',
        "spaced.resx": "<resheader name = 'resmimetype' >\n<value> text/microsoft-resx </value></resheader>",
        "attributes.resx": '<resheader name="resmimetype" xml:space="preserve"><value>text/microsoft-resx</value></resheader>',
        "different.resx": '<resheader name="resmimetype"><value>text/microsoft-resx-extra</value></resheader>',
        "wrong-header.resx": '<resheader name="other"><value>text/microsoft-resx</value></resheader>',
    }
    for name, header in headers.items():
        cases[name] = (("<?xml version='1.0'?>\n<root>" + header + "</root>").encode(),
                       {resx} if name in {"standard.resx", "spaced.resx", "attributes.resx"} else set())
    cases["ignored.dmg"] = (disk_image(True), {ignored})
    cases["raw.dmg"] = (disk_image(False), set())
    for name, data in [("compressed.zip", b"A" * 65536), ("empty-member.zip", b"")]:
        output = io.BytesIO()
        with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            archive.writestr("data.txt", data)
        cases[name] = (output.getvalue(), {expansion} if data else set())

    checked = {uri, bookmark, strings, remote, resx, expansion, ignored, masquerade}
    with tempfile.TemporaryDirectory(prefix="plist-improve-") as directory:
        work = Path(directory)
        for name, (data, _) in cases.items():
            (work / name).write_bytes(data)
        result = subprocess.run([engine, "--traits-dir", str(repo), "--format=json", str(work)],
                                capture_output=True, text=True, check=True)
        seen = set()
        for line in result.stdout.splitlines():
            for file in json.loads(line)["files"]:
                name = Path(file["path"]).name
                if name not in cases:  # ZIP members receive their own reports.
                    continue
                findings = file.get("traits", [])
                ids = {t["id"] for t in findings}
                assert ids & checked == cases[name][1], (name, ids & checked, cases[name][1])
                severe = {t["id"] for t in findings if t["crit"] >= 4}
                assert severe == ({masquerade} if name == "mixed.strings" else set()), (name, severe)
                seen.add(name)
        assert seen == cases.keys(), (seen, cases.keys())
    print(f"Plist improvement controls: {len(cases)} passed")


if __name__ == "__main__":
    main()
