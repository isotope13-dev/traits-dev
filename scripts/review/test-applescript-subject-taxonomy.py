#!/usr/bin/env python3
"""Check migrated AppleScript observations retain their evidence subjects."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cleave', default='../cleave/target/release/cleave')
args = parser.parse_args()
with tempfile.TemporaryDirectory(prefix='applescript-subject-') as tmp:
    root = Path(tmp)
    sample = root / 'sample.applescript'
    sample.write_text('set x to load script (POSIX file "/tmp/example.scpt")\n'
                      'open location "https://example.org"\n'
                      'do shell script "open -g /tmp/report; osacompile -e source"\n')
    result = subprocess.run(
        [str((repo / args.cleave).resolve()), '--traits-dir', str(repo), '--min-crit', 'component',
         '--format=json', str(sample)], check=True, capture_output=True, text=True,
    )
    report = json.loads(result.stdout.splitlines()[0])['files'][0]
    ids = {trait['id'] for trait in report.get('traits', [])}
    expected = {
        'micro-behaviors/os/module/load/path::load-script-posix-file',
        'micro-behaviors/communications/url/open::open-location-cmd',
        'micro-behaviors/os/handler/open::open-g-flag',
        'micro-behaviors/process/create/shell/command-string::shell-command-text-reference',
        'well-known/app/system/apple/macos-system-binaries::osacompile-cmd',
    }
    assert expected <= ids, expected - ids
    assert not any(i.startswith('micro-behaviors/process/create/script/apple-event::') and
                   i.rsplit('::', 1)[-1] in {x.rsplit('::', 1)[-1] for x in expected} for i in ids)
    print('AppleScript observations match in their new subject homes.')
