#!/usr/bin/env python3
"""Check Ruby command-source, response-stream and screenshot bindings statically."""
import argparse
import json
import lzma
import os
import re
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
REMOTE = 'objectives/command-and-control/remote-command/dispatch/command::ruby-socket-open3-command-shell'
POLL = 'objectives/command-and-control/backdoor/tasking/http::ruby-line-polled-cmd-powershell-backdoor'
SHOT = 'objectives/exfiltration/stealer/media::ruby-command-backdoor-screenshot-exfiltration'


def objects(text):
    decoder = json.JSONDecoder()
    offset = 0
    while offset < len(text):
        while offset < len(text) and text[offset].isspace():
            offset += 1
        if offset == len(text):
            break
        value, offset = decoder.raw_decode(text, offset)
        yield value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cleave', default=os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave')))
    args = parser.parse_args()
    fixture = ROOT / 'testdata/hostile/generated/ruby-triage'
    reverse = (fixture / 'reverse-command.rb').read_text()
    windows = (fixture / 'windows-polling.rb').read_text()
    cases = {
        'reverse.rb': (reverse, {REMOTE}, set(), True),
        'bind.rb': ((fixture / 'bind-command.rb').read_text(), {REMOTE}, set(), True),
        'windows.rb': (windows, {POLL, SHOT}, set(), True),
        'web.rb': (lzma.decompress((fixture / 'http-file-manager.rb.xz').read_bytes()).decode(), set(), set(), True),
        'different-input.rb': (reverse.replace('Open3.popen2e("#{line}")', 'Open3.popen2e("#{local_command}")'), set(), {REMOTE}, False),
        'different-stream.rb': (reverse.replace('IO.copy_stream(stdout_and_stderr, sock)', 'IO.copy_stream(stdout_and_stderr, $stdout)'), set(), {REMOTE}, False),
        'local-input-helper.rb': (windows.replace('-X GET #{url}', '-X GET /local-file'), set(), {POLL, SHOT}, False),
        'unrelated-post-data.rb': (windows.replace('Base64.encode64(data)', 'Base64.encode64(local_data)'), set(), {POLL, SHOT}, False),
        'different-shot.rb': (windows.replace('post($URL, clientUrl, filename)', 'post($URL, clientUrl, other_filename)'), {POLL}, {SHOT}, False),
        'renamed-helpers.rb': (re.sub(r'\bshell\b', 'launch_shell', windows.replace('executor', 'launch_task').replace('warLoop', 'poll_loop')), {POLL, SHOT}, set(), True),
    }
    for path in sorted((ROOT / 'testdata/notable/controls/ruby-triage').glob('*.rb')):
        cases[path.name] = (path.read_text(), set(), {REMOTE, POLL, SHOT}, False)
    with tempfile.TemporaryDirectory(prefix='ruby-triage-') as work:
        paths = []
        for name, (source, *_rest) in cases.items():
            path = Path(work) / name
            path.write_text(source)
            paths.append(str(path))
        result = subprocess.run([args.cleave, '--traits-dir', str(ROOT), '--format=json', *paths], text=True, capture_output=True, check=True)
        observed = {}
        for report in objects(result.stdout):
            for item in report['files']:
                observed[Path(item['path']).name] = item.get('traits', [])
        for name, (_source, required, forbidden, hostile) in cases.items():
            traits = observed[name]
            ids = {item['id'] for item in traits}
            assert required <= ids, (name, 'missing', required - ids)
            assert not forbidden & ids, (name, 'unexpected', forbidden & ids)
            if hostile:
                dirs = {item['id'].split('::')[0] for item in traits if item['crit'] == 5}
                assert len(dirs) >= 2, (name, 'needs two hostile directories', dirs)
            if name.endswith('.rb') and name in {p.name for p in (ROOT / 'testdata/notable/controls/ruby-triage').glob('*.rb')}:
                assert not [item for item in traits if item['crit'] >= 4], (name, 'control has threat findings')
    print(f'Ruby binding regressions passed: {len(cases)} cases')


if __name__ == '__main__':
    main()
