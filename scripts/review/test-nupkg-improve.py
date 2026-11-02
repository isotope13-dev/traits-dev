#!/usr/bin/env python3
"""Check honest metadata/identity findings and preserved attack detections."""

import argparse
import json
from pathlib import Path
import struct
import subprocess
import tempfile
import zipfile


def timestamp_variant(original, header_time, debug_time):
    data = bytearray(original)
    pe = struct.unpack_from("<I", data, 0x3C)[0]
    struct.pack_into("<I", data, pe + 8, header_time)
    optional = pe + 24
    directory = optional + (112 if struct.unpack_from("<H", data, optional)[0] == 0x20B else 96)
    debug_rva, debug_size = struct.unpack_from("<II", data, directory + 6 * 8)
    if debug_time is None:
        struct.pack_into("<II", data, directory + 6 * 8, 0, 0)
        return bytes(data)
    sections = optional + struct.unpack_from("<H", data, pe + 20)[0]
    for index in range(struct.unpack_from("<H", data, pe + 6)[0]):
        virtual_size, rva, raw_size, raw_offset = struct.unpack_from("<IIII", data, sections + index * 40 + 8)
        if rva <= debug_rva < rva + max(virtual_size, raw_size):
            debug_offset = raw_offset + debug_rva - rva
            for offset in range(debug_offset, debug_offset + debug_size, 28):
                struct.pack_into("<I", data, offset + 4, debug_time)
            return bytes(data)
    raise AssertionError("The reviewed PE fixture has no mapped debug directory")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cleave", default="../cleave/target/release/cleave")
    parser.add_argument("--samples-root", type=Path, action="append")
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[2]
    engine = str((repo / args.cleave).resolve())
    popen = "micro-behaviors/process/create/shell/command-mode::python-popen-command-call"
    concat = "micro-behaviors/data/string/concat/expression::python-popen-token-concatenation"
    service = "objectives/command-and-control/backdoor/tasking/command-http::python-http-json-command-execution-service"
    timestamps = "metadata/binary/provenance/build::future-pe-debug-timestamps"
    mismatch = "metadata/binary/debug::pe-stem-differs-from-pdb-stem"
    manifest = "well-known/app/development/lyric::lyric-dotnet-tool-manifest"
    lyric_package = "well-known/app/development/lyric::lyric-package-name"
    template = "metadata/package/files/nuget::nupkg-project-template-member"
    transitive = "metadata/package/files/nuget::nupkg-transitive-build-targets-member"
    checked = {popen, concat, service, timestamps, mismatch, manifest, lyric_package, template, transitive}
    retired = {"objectives/evasion/indicator-removal/timestamps::future-pe-debug-timestamps",
               "objectives/evasion/masquerade/debug::pe-stem-differs-from-pdb-stem",
               "objectives/command-and-control/backdoor/tasking/command-http::python-popen-command-call",
               "objectives/command-and-control/backdoor/tasking/command-http::python-obfuscated-popen-attribute"}
    server = '''from http.server import BaseHTTPRequestHandler
import os, json
class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        payload = json.loads(self.rfile.read(100))
        command = payload.get("query")
        result = os.popen(command).read()
        self.wfile.write(json.dumps({"stdout": result, "code": 0}).encode())
'''
    cases = {
        "shell.py": (b'import os\ncommand = "echo status"\nresult = os.popen(command).read()\n', {popen}),
        "concat.py": (b'attribute = "po" + "pen"\n', {concat}),
        "service.py": (server.encode(), {popen, service}),
        "joined-service.py": (server.replace("os.popen(command)", 'getattr(os, "po" + "pen")(command)').encode(), {concat, service}),
    }
    tool = '''<?xml version="1.0"?><DotNetCliTool Version="1"><Commands>
<Command Name="{name}" EntryPoint="{entry}.dll" Runner="dotnet" />
</Commands></DotNetCliTool>'''
    cases["other/DotnetToolSettings.xml"] = (tool.format(name="fkh", entry="fkh").encode(), set())
    cases["lyric/DotnetToolSettings.xml"] = (tool.format(name="lyric", entry="Lyric.Lyric").encode(), {manifest})
    cases["comment/DotnetToolSettings.xml"] = (("<?xml version='1.0'?><DotNetCliTool><!--" +
        '<Command Name="lyric" EntryPoint="Lyric.dll" Runner="dotnet" />' +
        "--></DotNetCliTool>").encode(), set())
    with tempfile.TemporaryDirectory(prefix="nupkg-improve-controls-") as directory:
        work = Path(directory)
        for name, (body, _) in cases.items():
            path = work / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(body)
        for filename, package_id, members, expected in [
            ("renamed.nupkg", "Lyric", {}, {lyric_package}),
            ("lyric.9.9.9.nupkg", "OtherTool", {}, set()),
            ("content.nupkg", "Example", {"templates/App.csproj": "<Project />",
                                            "buildTransitive/Example.targets": "<Project />"}, {template, transitive}),
            ("near-miss.nupkg", "Example", {"docs/templates/App.csproj": "<Project />",
                                             "build/Example.targets": "<Project />"}, set()),
        ]:
            with zipfile.ZipFile(work / filename, "w") as archive:
                archive.writestr("Example.nuspec", "<package><metadata><id>" + package_id +
                                 "</id><version>1.0.0</version><authors>Example</authors>"
                                 "<description>Control</description></metadata></package>")
                for member, body in members.items():
                    archive.writestr(member, body)
            cases[filename] = (b"", expected)
        if args.samples_root:
            package = next(p for root in args.samples_root for p in root.rglob("costura.fody.4.1.0.nupkg"))
            with zipfile.ZipFile(package) as archive:
                original = archive.read("weaver/Costura.Fody.dll")
            # The post-2030 header and post-2024 debug thresholds differ.
            for name, header, debug, expected in [
                ("future.dll", 2208988800, 1767225600, {timestamps, mismatch}),
                ("older-debug.dll", 2208988800, 1420070400, {mismatch}),
                ("older-header.dll", 1577836800, 1767225600, {mismatch}),
                ("no-debug.dll", 2208988800, None, set()),
                ("Costura.Fody.dll", 1577836800, 1767225600, set()),
            ]:
                (work / name).write_bytes(timestamp_variant(original, header, debug))
                cases[name] = (b"", expected)
        result = subprocess.run([engine, "--traits-dir", str(repo), "--format=json", str(work)],
                                capture_output=True, text=True, check=True)
        seen = set()
        for line in result.stdout.split("\n"):
            if not line:
                continue
            file = json.loads(line)["files"][0]
            name = str(Path(file["path"]).relative_to(work))
            if name not in cases:
                continue
            ids = {t["id"] for t in file.get("traits", [])}
            assert ids & checked == cases[name][1], (name, ids & checked, cases[name][1])
            assert not ids & retired, (name, ids & retired)
            if name in {"other/DotnetToolSettings.xml", "comment/DotnetToolSettings.xml", "lyric.9.9.9.nupkg"}:
                assert not any(i.startswith("well-known/app/development/lyric::") for i in ids), (name, ids)
            if name in {"service.py", "joined-service.py"}:
                assert any(t["id"] == service and t["crit"] == 5 for t in file["traits"])
            seen.add(name)
        assert seen == cases.keys(), (seen, cases.keys())
    print(f"NuGet improvement controls: {len(cases)} passed")


if __name__ == "__main__":
    main()
