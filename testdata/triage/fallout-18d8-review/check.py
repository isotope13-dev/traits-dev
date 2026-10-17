"""Check saved reports without executing specimens or contacting endpoints.

Generate controls with cleave --traits-dir . --format json <this directory>.
Usage: python3 check.py CONTROL_REPORT ATOMSCAN_MSI ATOMSCAN_NATIVE ATOMSCAN_UPX
"""
import json
from pathlib import Path
import sys


def objects(path):
    text = Path(path).read_text()
    decoder = json.JSONDecoder()
    while text.strip():
        text = text.lstrip()
        obj, end = decoder.raw_decode(text)
        yield obj
        text = text[end:]


SC = 'well-known/dual-use/remote-admin/screenconnect::'
QUERY = 'micro-behaviors/communications/url/query::h-name-p-number-parameters'
ROTATION = 'micro-behaviors/fs/write/file/executable::self-hash-rotation-relaunch'
REMOVED = 'micro-behaviors/os/autorun/login-items::self-mutating-elevated-run-autostart'
EXPECT = {
    'quiet.xml': ({SC + 'msi-stealth-access-group'}, set()),
    'visible.xml': (set(), {SC + 'msi-stealth-access-group'}),
    'unrelated.xml': (set(), {SC + 'msi-stealth-access-group'}),
    'neighboring-values.xml': (set(), {
        SC + 'msi-balloon-connect-hidden', SC + 'msi-balloon-hide-hidden',
        SC + 'msi-tray-icon-hidden', SC + 'msi-stealth-access-group'}),
    'consent-disabled.xml': (set(), {
        SC + 'msi-user-absent-auto-consent', SC + 'msi-backstage-auto-consent',
        SC + 'msi-unattended-consent-group'}),
    'consent-enabled.xml': ({SC + 'msi-unattended-consent-group'}, set()),
    'self-hosted-relay.xml': ({QUERY, SC + 'msi-screenconnect-relay-config'}, set()),
    'cloud-relay.xml': ({QUERY, SC + 'msi-screenconnect-relay-config'}, set()),
    'missing-port.xml': (set(), {QUERY, SC + 'msi-screenconnect-relay-config'}),
}


def main():
    assert len(sys.argv) == 5, __doc__
    observed = set()
    for report in objects(sys.argv[1]):
        for file in report['files']:
            name = Path(file['path']).name
            if name not in EXPECT:
                continue
            ids = {t['id'] for t in file.get('traits', [])}
            required, forbidden = EXPECT[name]
            assert required <= ids, (name, required - ids)
            assert not forbidden & ids, (name, forbidden & ids)
            observed.add(name)
    assert observed == set(EXPECT), set(EXPECT) - observed
    for index, path in enumerate(sys.argv[2:]):
        report, = objects(path)
        files = report['raw']['files']
        ids = {t['id'] for f in files for t in f.get('traits', [])}
        unusual = {t['id'] for f in files for t in f.get('traits', [])
                   if t['crit'] >= 4}
        expected = SC + 'msi-stealth-access-group' if index == 0 else ROTATION
        assert unusual == {expected}, (index, unusual)
        assert REMOVED not in ids
        if index == 0:
            assert SC + 'msi-screenconnect-relay-config' in ids
            assert SC + 'msi-screenconnect-unattended-installer' not in ids
    print('PASS: 9 configuration controls and 3 sample reports')


if __name__ == '__main__':
    main()
