#!/usr/bin/env python3
"""Distinguish parsed shortcut targets from incidental executable-path text."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cleave', default='../cleave/target/release/cleave')
args = parser.parse_args()
source = (repo / 'testdata/notable/lnk-stage-controls/cmd-echo.lnk').read_bytes()
ftp_source = (repo / 'testdata/hostile/bitter-paprat-8197/variant_ftp_proxy.lnk').read_bytes()
assert ftp_source.count(b'ftp.exe') == 1
needle = b'\\cmd.exe'
assert source.count(needle) == 1
with tempfile.TemporaryDirectory(prefix='shortcut-target-') as tmp:
    root = Path(tmp)
    samples = {
        'cmd.lnk': source,
        # Keep the link layout and string lengths intact, but change the basename.
        'differentcmd.lnk': source.replace(needle, b'xcmd.exe', 1),
        'embedded-wscript.lnk': source + b'\\Windows\\System32\\wscript.exe\0',
        'ftp.lnk': ftp_source,
        'other-s-option.lnk': ftp_source.replace(b'ftp.exe', b'zip.exe', 1),
    }
    for name, data in samples.items():
        (root / name).write_bytes(data)
    result = subprocess.run(
        [str((repo / args.cleave).resolve()), '--traits-dir', str(repo), '--format=json',
         *(str(root / name) for name in samples)], check=True, capture_output=True, text=True,
    )
    reports = [json.loads(line)['files'][0] for line in result.stdout.splitlines() if line]
    ids = {Path(r['path']).name: {t['id'] for t in r.get('traits', [])} for r in reports}
    assert set(ids) == set(samples), ids.keys()
    cmd = 'micro-behaviors/process/config/target::lnk-cmd-target'
    wscript_text = 'micro-behaviors/fs/path/executable::lnk-wscript-path-text'
    script_host = 'micro-behaviors/process/config/target::lnk-script-host-target'
    assert cmd in ids['cmd.lnk'] and cmd not in ids['differentcmd.lnk']
    assert cmd in ids['embedded-wscript.lnk'] and wscript_text in ids['embedded-wscript.lnk']
    assert script_host not in ids['embedded-wscript.lnk']
    option = 'micro-behaviors/process/argument/short-option::lnk-short-s-option'
    ftp_target = 'micro-behaviors/process/config/target::lnk-ftp-target'
    ftp_proxy = 'objectives/execution/lnk/proxy::ftp-script-proxy-shortcut'
    assert option in ids['ftp.lnk'] and option in ids['other-s-option.lnk']
    assert ftp_target in ids['ftp.lnk'] and ftp_target not in ids['other-s-option.lnk']
    assert ftp_proxy in ids['ftp.lnk'] and ftp_proxy not in ids['other-s-option.lnk']
    print('Shortcut target basenames and incidental path text are distinguished.')
