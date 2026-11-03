#!/usr/bin/env python3
"""Keep Lua startup configuration distinct from a CreateProcess call."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cleave', default='../cleave/target/release/cleave')
args = parser.parse_args()
flag = 'micro-behaviors/process/config/launch::lua-startup-showwindow-flag'
launch = 'micro-behaviors/process/create/exec::lua-createprocess-call'
with tempfile.TemporaryDirectory(prefix='lua-process-config-') as tmp:
    root = Path(tmp)
    config = 'local startup = {}\nstartup.dwFlags = win32.STARTF_USESHOWWINDOW\n'
    (root / 'config.lua').write_text(config)
    (root / 'launch.lua').write_text(config + 'win32.CreateProcessW(application)\n')
    result = subprocess.run(
        [str((repo / args.cleave).resolve()), '--traits-dir', str(repo),
         '--format=json', str(root / 'config.lua'), str(root / 'launch.lua')],
        check=True, capture_output=True, text=True,
    )
    reports = [json.loads(line)['files'][0] for line in result.stdout.splitlines() if line]
    seen = {Path(report['path']).name: {t['id'] for t in report.get('traits', [])} for report in reports}
    assert set(seen) == {'config.lua', 'launch.lua'}, seen.keys()
    assert flag in seen['config.lua'] and launch not in seen['config.lua'], seen['config.lua']
    assert flag in seen['launch.lua'] and launch in seen['launch.lua'], seen['launch.lua']
    print('Lua launch configuration and process call remain distinct.')
