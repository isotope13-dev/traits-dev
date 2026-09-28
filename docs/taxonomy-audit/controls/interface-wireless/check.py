"""Build inert PE data/export fixtures and scan them; never execute the DLLs.

Run without flags to compare against the checked-in pre-move baseline.
--before is for capturing that baseline before a migration. Requires clang and
lld-link. Generated DLLs and scan logs live outside the repository.
"""
from pathlib import Path
import argparse
import concurrent.futures
import json
import re
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--before', action='store_true')
parser.add_argument('--work', type=Path, default=Path('/tmp/taxonomy-interface-wireless/controls'))
args = parser.parse_args()
root = Path(__file__).resolve().parents[4]
engine = root.parent / 'cleave/target/release/cleave'
args.work.mkdir(parents=True, exist_ok=True)
old = 'micro-behaviors/os/network/interface'
wireless = 'micro-behaviors/hardware/wireless/network'
names = ['wlan-open-handle', 'wlan-enum-interfaces', 'wlan-get-available-network-list',
         'wlan-get-profile-list', 'wlan-get-profile', 'wlan-query-interface',
         'wlan-api-library-reference', 'wlan-api-provider',
         'bluetooth-find-first-radio', 'bluetooth-find-first-device',
         'wlan-network-recon', 'wlan-profile-enumeration',
         'wlan-bssid-profile-harvest', 'bluetooth-device-recon']
rules = [old + '::' + n if args.before else wireless + '::' + n for n in names]
rules += [old + '::get-adapters-info', old + '::host-network-fingerprint-surface',
          'objectives/exfiltration/messaging/webhook::webhook-with-system-data-host-2']
profile = b'wlanapi.dll\0WlanGetProfileList\0WlanGetProfile\0'
field = b'webhook "ip": "192.0.2.1"\0'
cases = {
    'profile': (profile + field, []),
    'profile-only': (profile, []),
    'field-only': (field, []),
    'unrelated-wireless': (b'BSSID\0' + field, []),
    'far-profile': (profile + b'X' * 8192 + b'\0' + field, []),
    'adapter': (field, ['GetAdaptersInfo']),
    'bluetooth': (field, ['BluetoothFindFirstRadio', 'BluetoothFindFirstDevice']),
    'wlanapi': (b'WLAN provider control\0', ['WlanOpenHandle', 'WlanEnumInterfaces', 'WlanGetAvailableNetworkList']),
}
for name, (data, exports) in cases.items():
    target = args.work / (name + '.dll')
    if target.exists():
        continue
    source = args.work / (name + '.c')
    source.write_text('__declspec(dllexport) const unsigned char fixture_data[] = {' + ','.join(map(str, data)) + '};\n' +
                      ''.join('__declspec(dllexport) int ' + symbol + '(void) { return 0; }\n' for symbol in exports))
    obj = args.work / (name + '.obj')
    subprocess.run(['clang', '--target=x86_64-pc-windows-msvc', '-c', str(source), '-o', str(obj)], check=True, capture_output=True)
    subprocess.run(['lld-link', '/dll', '/noentry', '/nodefaultlib', '/opt:noref', '/out:' + str(target), str(obj)], check=True, capture_output=True)

def scan(name):
    run = subprocess.run([str(engine), '--traits-dir', str(root), 'test-rules', '--rules', ','.join(rules), str(args.work / (name + '.dll'))], text=True, capture_output=True, check=True)
    (args.work / (name + ('.before.log' if args.before else '.after.log'))).write_text(run.stdout + run.stderr)
    states = {}
    for line in run.stdout.splitlines():
        match = re.match(r'^(NOT MATCHED|MATCHED) (\S+) \((.*)\)', line)
        if match:
            states[match[2].split('::')[-1]] = [match[1], match[3]]
    assert len(states) == len(rules), (name, states, run.stdout[-2000:])
    return name, states

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    result = dict(pool.map(scan, cases))

key = 'webhook-with-system-data-host-2'
# Nearby profile/interface evidence supports the capability context. A field
# alone, unrelated wireless token, or distant profile must not acquire it.
for name, yes in [('profile', True), ('profile-only', False), ('field-only', False),
                  ('unrelated-wireless', False), ('far-profile', False)]:
    assert (result[name][key][0] == 'MATCHED') == yes, (name, result[name][key])
assert result['bluetooth']['bluetooth-device-recon'][0] == 'MATCHED'
assert result['wlanapi']['wlan-api-provider'][0] == 'MATCHED'
assert result['profile']['wlan-profile-enumeration'][0] == 'MATCHED'
baseline = Path(__file__).with_name('baseline.json')
if args.before:
    baseline.write_text(json.dumps(result, indent=2) + '\n')
else:
    expected = json.loads(baseline.read_text())
    assert result == expected, json.dumps({'before': expected, 'after': result}, indent=2)
print(f'{len(cases)} inert PE controls, {sum(map(len, result.values()))} rule verdicts verified' + (' and baseline saved' if args.before else ' against pre-move baseline'))
