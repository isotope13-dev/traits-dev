#!/usr/bin/env python3
"""Check inert resource metadata and preserve the SharePoint consumer."""

import json
import os
from pathlib import Path
import plistlib
import subprocess
import tempfile


def main():
    repo = Path(__file__).resolve().parents[2]
    engine = os.environ.get("CLEAVE", str(repo.parent / "cleave/target/release/cleave"))
    qualified = "System.Drawing.Color, System.Drawing, Version=4.0.0.0"
    fixtures = {
        "resource.resx": b"<?xml version='1.0' encoding='utf-8'?>\n<root><resheader name='resmimetype'>\n<value>text/microsoft-resx</value></resheader></root>",
        "reference.xml": f"<root><value>{qualified}</value></root>".encode(),
        "ordinary.xml": b"<root><value>System.Drawing.Color</value></root>",
        "bdc.xml": (f'<Model xmlns="http://schemas.microsoft.com/windows/2007/BusinessDataCatalog">'
                    f'<Property Name="Class">{qualified}</Property></Model>').encode(),
        "archive-xml.plist": plistlib.dumps({"$archiver": "NSKeyedArchiver"}),
        "archive-binary.plist": plistlib.dumps({"$archiver": "NSKeyedArchiver"}, fmt=plistlib.FMT_BINARY),
        "other.plist": plistlib.dumps({"$archiver": "OtherArchiver"}),
        "nested.plist": plistlib.dumps({"nested": {"$archiver": "NSKeyedArchiver"}}),
        "CodeResources": plistlib.dumps({"files2": {"Frameworks/Example.framework": {
            "requirement": 'identifier "com.bugsplat.BugsplatMac"'}}}),
    }
    expected = {
        "resource.resx": {"metadata/file/format/managed-runtime::resx-resource-mime-declaration"},
        "reference.xml": {"metadata/lang/runtime::dotnet-framework-assembly-type"},
        "bdc.xml": {"metadata/lang/runtime::dotnet-framework-assembly-type",
                    "micro-behaviors/data/serialize/object::sharepoint-bdcm-framework-class-property"},
        "archive-xml.plist": {"metadata/file/format/serialization::ns-keyed-archiver"},
        "archive-binary.plist": {"metadata/file/format/serialization::ns-keyed-archiver"},
        "CodeResources": {"metadata/binary/signing::coderesources-plist",
                          "metadata/package/dependencies/logging::bugsplat-mac-bundle-id-reference"},
    }
    with tempfile.TemporaryDirectory(prefix="plist-bad-controls-") as directory:
        work = Path(directory)
        for name, data in fixtures.items():
            (work / name).write_bytes(data)
        result = subprocess.run([engine, "--traits-dir", str(repo), "--format=json", str(work)],
                                capture_output=True, text=True, check=True)
        observed = {}
        for line in result.stdout.splitlines():
            for file in json.loads(line)["files"]:
                observed[Path(file["path"]).name] = file.get("traits", [])
        assert observed.keys() == fixtures.keys(), observed.keys()
        retired = {"micro-behaviors/data/serialize/object::dotnet-framework-assembly-type",
                   "well-known/lib/observability/bugsplat::bugsplat-mac-bundle-id-reference"}
        for name, traits in observed.items():
            ids = {trait["id"] for trait in traits}
            assert expected.get(name, set()) <= ids, (name, ids)
            assert not retired & ids, (name, ids)
            if name != "bdc.xml":
                assert not any(trait["crit"] >= 4 for trait in traits), (name, traits)
        archive_id = "metadata/file/format/serialization::ns-keyed-archiver"
        for name in ["other.plist", "nested.plist"]:
            assert not any(t["id"] == archive_id for t in observed[name]), (name, observed[name])
        assert not any(t["id"] == "metadata/lang/runtime::dotnet-framework-assembly-type"
                       for t in observed["ordinary.xml"])
    print("Plist triage controls: 9 passed")


if __name__ == "__main__":
    main()
