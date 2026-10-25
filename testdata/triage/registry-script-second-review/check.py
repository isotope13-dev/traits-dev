"""Static regression controls. Never execute specimens or contact their URLs."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
DECOY = 'objectives/evasion/decoy/social::'
CLEAN = 'objectives/evasion/indicator-removal/cleanup::batch-msi-error-decoy-script-cleanup'
SCREEN = 'objectives/exfiltration/stealer/screen::powershell-screen-archive-telegram-exfil'
CHAIN = 'micro-behaviors/process/deploy/file-exec::powershell-same-variable-outfile-launch'
POLL = 'micro-behaviors/process/lifecycle/supervise::powershell-process-polling-loop'
CONFIG = 'micro-behaviors/communications/http/services/telegram::telegram-hardcoded-bot-config'
LURE = 'objectives/execution/lure/clipboard/page::'
OLD_TASK = 'objectives/command-and-control/backdoor/control/telegram::telegram-polled-attachment-execution'


def documents(text):
    decoder = json.JSONDecoder()
    while text.strip():
        text = text.lstrip()
        report, end = decoder.raw_decode(text)
        yield report
        text = text[end:]


def cases():
    batch = (HERE / 'document-error-installer.bat').read_text()
    ps = (HERE / 'telegram-screen-stager.ps1').read_text()
    page = (ROOT / 'testdata/taxonomy/platform-clipboard-review/reserved-loader.html').read_text()
    yield 'renamed-installer.bat', batch, {CLEAN}, set()
    yield 'renamed-agent.bat', batch.replace('ScreenConnect.ClientSetup', 'OtherClient').replace('agent', 'package'), {CLEAN}, set()
    yield 'installer-error.bat', batch.replace('requested document could not be opened', 'requested installation has failed'), set(), {CLEAN, DECOY + 'document-error-with-quiet-msi-elevation', DECOY + 'batch-quiet-msi-fetch-install-error-decoy'}
    yield 'renamed-stager.ps1', ps.replace('$implant', '$destination').replace('telemetryhost.exe', 'helper.exe').replace('desktop.png', 'image.png'), {SCREEN, CHAIN}, {OLD_TASK, POLL}
    yield 'same-destination.ps1', 'Invoke-WebRequest -Uri $url -OutFile $destination\nStart-Process -FilePath $destination\n', {CHAIN}, set()
    yield 'different-destination.ps1', 'Invoke-WebRequest -Uri $url -OutFile $destination\nStart-Process -FilePath $other\n', set(), {CHAIN}
    yield 'rebound-destination.ps1', 'Invoke-WebRequest -Uri $url -OutFile $destination\n$destination = "other.exe"\nStart-Process -FilePath $destination\n', set(), {CHAIN}
    yield 'one-time-query.ps1', 'Get-Process\nwhile ($true) { Start-Sleep -Seconds 5 }', set(), {POLL}
    yield 'process-monitor.ps1', 'while ($true) { Get-Process -Name worker; Start-Sleep -Seconds 5 }', {POLL}, set()
    yield 'different-process-loop.ps1', 'while ($true) { Get-Process }\nwhile ($true) { Start-Sleep -Seconds 5 }', set(), {POLL}
    yield 'bot-config.ps1', '$botToken="1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghi"\n$chatId="-1002468135790"\n$api="https://api.telegram.org/bot$botToken"\n', {CONFIG}, {SCREEN, OLD_TASK}
    yield 'renamed-download.html', page.replace('id="download"', 'id="setup"').replace("getElementById('download')", "getElementById('setup')"), {LURE + 'macos-clipboard-remote-shell-loader', LURE + 'platform-switched-clipboard-loader'}, set()
    yield 'copy-command-tutorial.html', page.replace('Download for your computer', 'Copy installation command'), set(), {LURE + x for x in ['clickfix-clipboard-mshta-paste-run', 'clickfix-clipboard-mshta-run', 'macos-clipboard-remote-shell-loader', 'platform-switched-clipboard-loader']}


def main():
    with tempfile.TemporaryDirectory(prefix='script-second-review-') as directory:
        directory = Path(directory)
        expected = {}
        for name, content, required, forbidden in cases():
            path = directory / name
            path.write_text(content)
            expected[str(path)] = required, forbidden
        paths = list(expected)
        controls = [
            'testdata/benign/dotform-download-ui.html',
            'testdata/benign/csv-export-download.html',
            'testdata/benign/visible-exe-download.html',
            'testdata/taxonomy/platform-clipboard-review/honest-terminal-help.html',
            'testdata/taxonomy/platform-clipboard-review/platform-loader.html',
            'testdata/taxonomy/platform-clipboard-review/mshta-command-help.html',
            'testdata/rmm-staged-execution/approved-install.ps1',
            'testdata/rmm-staged-commands/remote-agent-staged.ps1',
            'testdata/hostile/registry-agent-second-review/telegram-agent.c',
            'testdata/hostile/telegram-desktop-lockdown.py',
            'testdata/benign/user-configured-telegram-bot-controls.py',
        ]
        paths += [str(ROOT / p) for p in controls]
        result = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir',
                                 os.environ.get('REVIEW_TRAITS', str(ROOT)), '--format', 'json', *paths],
                                capture_output=True, text=True, timeout=300,
                                env={**os.environ, 'CLEAVE_VALIDATE': '0'})
        assert result.returncode == 0, result.stderr
        assert 'ERROR' not in result.stderr and 'skipped' not in result.stderr, result.stderr
        reports = list(documents(result.stdout))
        all_files = [f for r in reports for f in r['files']]
        seen = set()
        for f in all_files:
            path = f['path']
            ids = {t['id'] for t in f.get('traits', [])}
            if path in expected:
                required, forbidden = expected[path]
                assert required <= ids, (path, 'missing', required - ids)
                assert not forbidden & ids, (path, 'unexpected', forbidden & ids)
                seen.add(path)
            elif path.endswith(('honest-terminal-help.html', 'mshta-command-help.html', 'dotform-download-ui.html', 'csv-export-download.html', 'visible-exe-download.html')):
                assert all(t['crit'] < 4 for t in f.get('traits', [])), path
            elif path.endswith(('telegram-agent.c', 'telegram-desktop-lockdown.py')):
                assert any(t['crit'] == 5 for t in f.get('traits', [])), (path, 'lost attack coverage')
        assert seen == set(expected), seen ^ set(expected)
        if os.environ.get('REVIEW_OUTPUT'):
            Path(os.environ['REVIEW_OUTPUT']).write_text(json.dumps(reports, indent=2))
        print(f'{len(expected)} focused controls and {len(controls)} existing fixtures passed')


if __name__ == '__main__':
    main()
