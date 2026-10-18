#!/usr/bin/env python3
"""Run behavioral controls outside fixture paths, which can suppress traits."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

root = Path(__file__).resolve().parents[2]
here = Path(__file__).resolve().parent
traffic = 'objectives/impact/ui/manipulation/traffic::'
browser = 'objectives/impact/ui/manipulation/browser::'
service = 'micro-behaviors/os/service/launchagent::'
calendar = 'micro-behaviors/time/query::php-named-timezone-weekday-hour-queries'
json_context = 'micro-behaviors/communications/http/response::php-json-variable-redirect-cooccurrence'
history = 'micro-behaviors/ui/window/navigation::history-push-popstate-cooccurrence'
cases = {
    'support-lock.html': (3, None, [browser + 'fullscreen-keyboard-exit-browser-lock', browser + 'back-button-history-redirect-trap']),
    'verification-update.php': (2, 0, [traffic + 'update-pretext-verification-redirect', traffic + 'update-verification-redirect-json-reads']),
    'verification-only.php': (0, 0, [calendar, json_context]),
    'launchagent.py': (0, 1, [service + 'source-launchagent-remote-shell-autorun', service + 'python-launchctl-shell-pipeline']),
    'fullscreen-editor.html': (0, 0, []),
    'history-router.html': (0, 0, [history]),
    'business-hours.php': (0, 0, [calendar]),
    'json-cache-redirect.php': (0, 0, [json_context]),
    'shop-url.php': (0, 0, ['micro-behaviors/communications/url/host/name::tld-shop']),
}
with tempfile.TemporaryDirectory(prefix='.support-review-', dir=root) as staging:
    targets = []
    for name in cases:
        target = Path(staging) / name
        shutil.copyfile(here / name, target)
        targets.append(str(target))
    result = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(root),
         '--format', 'json', *targets], capture_output=True, text=True,
    )
if result.returncode:
    raise RuntimeError(result.stdout + result.stderr)
decoder = json.JSONDecoder()
remaining = result.stdout.strip()
files = []
while remaining:
    report, consumed = decoder.raw_decode(remaining)
    files.extend(report['files'])
    remaining = remaining[consumed:].lstrip()
for file in files:
    name = Path(file['path']).name
    hostile, suspicious, required = cases[name]
    traits = {t['id']: t for t in file['traits']}
    assert set(required) <= traits.keys(), (name, 'missing', set(required) - traits.keys())
    assert sum(t['crit'] == 5 for t in traits.values()) == hostile, (name, 'hostile count')
    if suspicious is not None:
        assert sum(t['crit'] == 4 for t in traits.values()) == suspicious, (name, 'suspicious count')
    print(name, 'PASS')
assert len(files) == len(cases)
