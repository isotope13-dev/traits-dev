#!/usr/bin/env python3
"""Static RC4 APK recovery controls, including renamed assets and unused keys."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import subprocess
import struct
import sys
import tempfile
import zipfile
import zlib

sys.dont_write_bytecode = True
from apk_dex_fixture import string_dex


def rc4(data, key):
    state, j = list(range(256)), 0
    for i in range(256):
        j = (j + state[i] + key[i % len(key)]) % 256
        state[i], state[j] = state[j], state[i]
    out, i, j = bytearray(), 0, 0
    for value in data:
        i = (i + 1) % 256
        j = (j + state[i]) % 256
        state[i], state[j] = state[j], state[i]
        out.append(value ^ state[(state[i] + state[j]) % 256])
    return bytes(out)


def archive(members):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', compression=zipfile.ZIP_DEFLATED) as out:
        for name, data in members:
            out.writestr(name, data)
    return buffer.getvalue()


def without_nearby_text_reads(payload, calls, selectors):
    """Keep generic text reads, but remove those around the sensitive query."""
    count, offset = struct.unpack_from('<II', payload, 56)
    strings = []
    for i in range(count):
        at = struct.unpack_from('<I', payload, offset + 4 * i)[0]
        while payload[at] & 0x80:
            at += 1
        at += 1
        strings.append(payload[at:payload.index(0, at)].decode(errors='replace'))
    count, offset = struct.unpack_from('<II', payload, 64)
    types = [strings[struct.unpack_from('<I', payload, offset + 4 * i)[0]] for i in range(count)]
    count, offset = struct.unpack_from('<II', payload, 88)
    methods = {}
    for i in range(count):
        owner, _, name = struct.unpack_from('<HHI', payload, offset + 8 * i)
        methods[types[owner] + '->' + strings[name]] = i
    owner = 'Landroid/view/accessibility/AccessibilityNodeInfo;->'
    replacement = methods[owner + 'getContentDescription']
    queries = [call['offset'] for call in calls
               if call['target'] == owner + 'findAccessibilityNodeInfosByViewId'
               and any(arg.get('value') in selectors for arg in call['args'])]
    assert queries
    data = bytearray(payload)
    changed = remaining = 0
    for call in calls:
        if call['target'] != owner + 'getText':
            continue
        if not any(abs(call['offset'] - query) <= 512 for query in queries):
            remaining += 1
            continue
        at = call['offset']
        assert data[at] in (0x6e, 0x74), (at, data[at])
        assert struct.unpack_from('<H', data, at + 2)[0] == methods[owner + 'getText']
        struct.pack_into('<H', data, at + 2, replacement)
        changed += 1
    assert changed and remaining, (changed, remaining)
    data[12:32] = hashlib.sha1(data[32:]).digest()
    struct.pack_into('<I', data, 8, zlib.adler32(data[12:]) & 0xffffffff)
    return bytes(data)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cleave', default='../cleave/target/release/cleave')
    parser.add_argument('--samples-root', type=Path, required=True)
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[2]
    engine = str((repo / args.cleave).resolve())

    def member(prefix, name):
        paths = [p for p in args.samples_root.rglob('*.apk') if p.name.startswith(prefix)]
        assert len(paths) == 1, (prefix, paths)
        with zipfile.ZipFile(paths[0]) as source:
            info = source.getinfo(name)
            info.flag_bits &= ~1
            return source.read(info)

    wallet = 'objectives/credential-access/wallet/mnemonic::android-multi-wallet-phrase-ui-capture'
    auth = 'objectives/credential-access/capture/input::android-authenticator-ui-capture'
    recovery = 'metadata/archive/member/encoding::apk-rc4-recovered-code-asset'
    focus = {wallet, auth, recovery}
    actual = rc4(member('e29def53e832', 'assets/gqqd.json'), b'rqKu')
    with zipfile.ZipFile(io.BytesIO(actual)) as source:
        payload = source.read('classes.dex')
    manifest = member('6bb9994c7d0c', 'AndroidManifest.xml')
    benign = string_dex('ordinary benign payload')

    def apk(key, contents, *, referenced=True, key_source=True, asset='assets/blob.dat', first=False):
        members = [('AndroidManifest.xml', manifest)]
        if key_source:
            members.append(('classes.dex', string_dex(key.decode(), referenced)))
        entry = (asset, contents)
        members.insert(0, entry) if first else members.append(entry)
        return archive(members)

    key = b'a-rotated-independent-key'
    wrapped = archive([('renamed-code.bin', payload)])
    cases = {
        'changed-key-renamed-code.apk': (apk(key, rc4(wrapped, key)), focus),
        'asset-before-key-source.apk': (apk(key, rc4(wrapped, key), first=True), focus),
        'image-suffix-asset.apk': (apk(key, rc4(wrapped, key), asset='assets/ordinary-image.jpg'), focus),
        'direct-dex-asset.apk': (apk(key, rc4(payload, key)), focus),
        'unicode-key.apk': (apk('密钥'.encode(), rc4(wrapped, '密钥'.encode())), focus),
        'benign-code-asset.apk': (apk(key, rc4(benign, key)), {recovery}),
        'benign-zip-code.apk': (apk(key, rc4(archive([('component.bin', benign)]), key)), {recovery}),
        'wrong-key.apk': (apk(b'wrong-independent-key', rc4(wrapped, key)), set()),
        'unused-pool-key.apk': (apk(key, rc4(wrapped, key), referenced=False), set()),
        'missing-dex-source.apk': (apk(key, rc4(wrapped, key), key_source=False), set()),
        'non-code-zip.apk': (apk(key, rc4(archive([('notes.txt', b'ordinary data')]), key)), set()),
    }
    bad_crc = bytearray(wrapped)
    cd = bad_crc.index(b'PK\x01\x02')
    bad_crc[cd + 16] ^= 1
    cases['bad-inner-crc.apk'] = (apk(key, rc4(bad_crc, key)), set())
    bad_dex = bytearray(payload)
    bad_dex[12] ^= 1
    cases['bad-inner-dex-digest.apk'] = (apk(key, rc4(bad_dex, key)), set())

    with tempfile.TemporaryDirectory(prefix='apk-call-controls-') as directory:
        path = Path(directory) / 'payload.dex'
        path.write_bytes(payload)
        facts = subprocess.run([engine, 'facts', 'calls', '--json', str(path)],
                               capture_output=True, text=True, check=True)
        calls = json.loads(facts.stdout)
    without_wallet = without_nearby_text_reads(payload, calls, {
        'com.bitcoin.mwallet:id/mnemonicTable', 'com.wallet.crypto.trustapp:id/phrase'})
    without_auth = without_nearby_text_reads(payload, calls, {
        'com.google.android.apps.authenticator2:id/user_row_drag_handle'})
    cases['wallet-only-distant-text-reads.apk'] = (apk(key, rc4(without_wallet, key)), {auth, recovery})
    cases['auth-only-distant-text-reads.apk'] = (apk(key, rc4(without_auth, key)), {wallet, recovery})
    # A manifest/reference document is not an implemented banking controller.
    cases['permission-only-interfaces.xml'] = (b'''<manifest xmlns:android="http://schemas.android.com/apk/res/android" package="org.example.smshelper">
<uses-permission android:name="android.permission.SEND_SMS"/>
<uses-permission android:name="android.permission.READ_SMS"/>
<application><service android:name="org.example.AccessibilityHelper" android:permission="android.permission.BIND_ACCESSIBILITY_SERVICE">
<meta-data android:name="interface" android:value="Landroid/accessibilityservice/AccessibilityService; Landroid/telephony/SmsManager;"/>
</service><receiver android:name="org.example.BootReceiver"><intent-filter><action android:name="android.intent.action.BOOT_COMPLETED"/></intent-filter></receiver></application>
</manifest>''', set())
    cases['number-referenced.dex'] = (string_dex('1065-71090-88877'), set())
    cases['number-unreferenced.dex'] = (string_dex('1065-71090-88877', referenced=False), set())
    cases['number-ordinary-identifier.dex'] = (string_dex('10657109088877'), set())

    with tempfile.TemporaryDirectory(prefix='apk-rc4-controls-') as directory:
        work = Path(directory)
        for name, (data, _) in cases.items():
            (work / name).write_bytes(data)
        result = subprocess.run([engine, '--traits-dir', str(repo), '--format=json', str(work)],
                                capture_output=True, text=True, check=True)
        assert 'skipped' not in result.stderr, result.stderr
        seen = set()
        for line in result.stdout.split('\n'):
            if not line.strip():
                continue
            report = json.loads(line)
            files = report['files']
            root = next(file for file in files if file['id'] == 0)
            name = Path(root['path']).name
            traits = {t['id']: t for file in files for t in file.get('traits', [])}
            actual = traits.keys() & focus
            assert actual == cases[name][1], (name, actual, cases[name][1])
            if recovery in actual:
                assert traits[recovery]['crit'] == 4, (name, traits[recovery])
            if not ({wallet, auth} & cases[name][1]):
                severe = {t['id'] for t in traits.values() if t['crit'] >= 4}
                assert severe == actual & {recovery}, (name, 'unexpected severe finding', severe)
                assert not [t for t in traits.values() if t['crit'] >= 5], (name, 'false hostile finding')
            if name == 'permission-only-interfaces.xml':
                required = {
                    'metadata/binary/symbols/descriptor::android-sms-manager-descriptor',
                    'metadata/binary/symbols/descriptor::android-accessibility-service-descriptor',
                    'metadata/permission/network::android-send-sms-request-source',
                    'metadata/permission/storage::android-read-sms-request-source',
                    'metadata/package/entrypoint/event::android-boot-completed-action-source',
                }
                assert required <= traits.keys(), required - traits.keys()
            if name.startswith('number-'):
                number = 'metadata/lang/source/literal/string/shape::dex-106-series-number-constant'
                assert (number in traits) == (name == 'number-referenced.dex'), name
            seen.add(name)
        assert seen == cases.keys(), (seen, cases.keys())
    print(f'APK RC4 recovery controls: {len(cases)} passed')


if __name__ == '__main__':
    main()
