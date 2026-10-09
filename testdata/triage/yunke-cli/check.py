"""Focused positive and near-miss checks for Yunke triage corrections."""
import json
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parents[3]
fixtures = Path(__file__).resolve().parent
result = subprocess.run(
    ['cleave', '--traits-dir', str(root), '--format', 'json',
     str(fixtures / 'observations.js'), str(fixtures / 'near-miss.js')],
    check=True, capture_output=True, text=True,
)
remaining = result.stdout
reports = []
decoder = json.JSONDecoder()
while remaining.strip():
    report, length = decoder.raw_decode(remaining.lstrip())
    remaining = remaining.lstrip()[length:]
    reports.append(report)
ids = [{trait['id'] for file in report['files'] for trait in file['traits']}
       for report in reports]
expected = {
    'micro-behaviors/communications/http/request/client::npm-registry-metadata-request',
    'micro-behaviors/communications/socket/bind/address::bind-loopback-address',
    'micro-behaviors/communications/http/server/lifecycle::response-finish-post-hook',
    'micro-behaviors/data/codec::base64-helper-invocation',
    'micro-behaviors/fs/path/storage::android-sdcard-path-reference',
    'micro-behaviors/os/env/runtime::node-options-child-env-override',
}
assert expected <= ids[0], expected - ids[0]
assert not expected & ids[1], expected & ids[1]
assert not any('pino-worker-env' in item or 'electron-remote-control-loopback' in item
               for found in ids for item in found)
print('Positive and near-miss controls passed')
