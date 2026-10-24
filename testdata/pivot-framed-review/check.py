"""Check source-to-sink boundaries using static scans; never execute fixtures."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent

def decode_reports(path):
    source = Path(path).read_text()
    decoder = json.JSONDecoder()
    files = {}
    while source.strip():
        report, length = decoder.raw_decode(source.lstrip())
        source = source.lstrip()[length:]
        for entry in report['files']:
            files[Path(entry['path']).name] = entry
    return files

def suffixes(entry, minimum=0):
    return {t['id'].split('::')[-1] for t in entry['traits'] if t['crit'] >= minimum}

parser = argparse.ArgumentParser()
parser.add_argument('--after', type=Path)
parser.add_argument('--before', type=Path)
parser.add_argument('--record', type=Path)
args = parser.parse_args()
if args.after:
    after = decode_reports(args.after)
else:
    with tempfile.TemporaryDirectory() as temporary:
        target = Path(temporary) / 'reports.json'
        subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
                        str(HERE / 'fixtures'), '--format', 'json', '-o', str(target)], check=True)
        after = decode_reports(target)

required = {'node-framed-tls-pivot-rat', 'fortios-credential-harvesting-command-agent',
            'sysinfo-exfil-socket', 'node-framed-appliance-config-export',
            'node-framed-channel-shell-relay'}
assert required <= suffixes(after['framed-agent.js'], 5)
for name, absent in [('different-file-map.js', 'node-framed-appliance-config-export'),
                     ('different-ps-output.js', 'sysinfo-exfil-socket'),
                     ('without-shell-input.js', 'node-framed-channel-shell-relay'),
                     ('wrong-channel-bytes.js', 'node-framed-channel-shell-relay')]:
    actual = suffixes(after[name], 5)
    assert absent not in actual, (name, absent)
    assert required - {absent} <= actual, (name, actual)
for name in ['independent-operations.js', 'type-selectors.js']:
    assert not suffixes(after[name], 4), (name, suffixes(after[name], 4))
assert 'js-dns-oast-json-profile-exfil' in suffixes(after['dns-json-label.js'], 5)
assert 'node-base64-buffer-query' in suffixes(after['dns-json-label.js'])
assert 'node-event-callback-shell-bridge' in suffixes(after['direct-stream-relay.js'], 5)
assert 'child-output-callback-relays-data' in suffixes(after['direct-stream-relay.js'])

if args.before:
    before = decode_reports(args.before)
    assert 'sysinfo-exfil-socket' in suffixes(before['independent-operations.js'], 5)
    assert 'js-json-base64-dns-label' in suffixes(before['independent-operations.js'])
    for name in ['framed-agent.js', 'dns-json-label.js', 'direct-stream-relay.js']:
        assert suffixes(before[name], 5) <= suffixes(after[name], 5), name

record = {name: {'hostile': sum(t['crit'] == 5 for t in entry['traits']),
                 'suspicious': sum(t['crit'] == 4 for t in entry['traits']),
                 'hostile_ids': sorted(suffixes(entry, 5))}
          for name, entry in after.items()}
if args.record:
    args.record.write_text(json.dumps(record, indent=2) + '\n')
print(f'Passed {len(after)} positive and boundary controls; retained baseline attacks.')
