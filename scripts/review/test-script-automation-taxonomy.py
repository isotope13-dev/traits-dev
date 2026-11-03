#!/usr/bin/env python3
"""Check moved browser and application-automation evidence."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cleave', default='../cleave/target/release/cleave')
args = parser.parse_args()
with tempfile.TemporaryDirectory(prefix='script-automation-') as tmp:
    root = Path(tmp)
    cases = {
        'browser.py': 'from playwright.sync_api import sync_playwright\npage.evaluate("1")\nchromium.launch()\ncopy_chrome_profile()\n',
        'browser.js': 'import {connect} from "./cdp-bootstrap.js";\nfunction withCdpPage() {}\nfunction evaluate() {}\npage.evaluate("1");\n',
        'events.applescript': 'tell application "System Events" to keystroke "x"\n',
        'negative.py': 'def evaluate(x): return x\n',
    }
    for name, source in cases.items():(root / name).write_text(source)
    result = subprocess.run(
        [str((repo / args.cleave).resolve()), '--traits-dir', str(repo), '--min-crit', 'component',
         '--format=json', *(str(root / name) for name in cases)],
        check=True, capture_output=True, text=True,
    )
    reports = [json.loads(line)['files'][0] for line in result.stdout.splitlines() if line]
    ids = {Path(r['path']).name: {t['id'] for t in r.get('traits', [])} for r in reports}
    assert set(ids) == set(cases), ids.keys()
    py_expected = {
        'well-known/lib/platform/browser-automation/frameworks::playwright-python-sync-api-import',
        'micro-behaviors/process/interpreter/eval/direct::python-page-evaluate-call',
        'micro-behaviors/os/application/control::python-chromium-launch-call',
        'micro-behaviors/fs/directory/copy::chrome-profile-copy-name-text',
    }
    js_expected = {
        'micro-behaviors/process/interpreter/eval/direct::browser-page-evaluate',
        'metadata/file/profile/browser/automation::browser-cdp-evaluate-adapter',
    }
    system = 'micro-behaviors/os/application/target/system::system-events-target'
    assert py_expected <= ids['browser.py'], py_expected - ids['browser.py']
    assert js_expected <= ids['browser.js'], js_expected - ids['browser.js']
    assert system in ids['events.applescript'], ids['events.applescript']
    assert not py_expected & ids['negative.py'], ids['negative.py']
    print('Browser evaluation, product imports, profile names and System Events remain distinct.')
