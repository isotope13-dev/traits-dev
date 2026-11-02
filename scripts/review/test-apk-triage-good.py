#!/usr/bin/env python3
"""Static APK regression controls; specimens are decoded and scanned, never run."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import struct
import subprocess
import tempfile
import zipfile
import zlib


def checksum(blob):
    blob = bytearray(blob)
    blob[12:32] = hashlib.sha1(blob[32:]).digest()
    struct.pack_into('<I', blob, 8, zlib.adler32(blob[12:]) & 0xffffffff)
    return bytes(blob)


def rc4(blob, key):
    """Analyst-derived payload transformation, with no specimen execution."""
    state = list(range(256))
    j = 0
    for i in range(256):
        j = (j + state[i] + key[i % len(key)]) % 256
        state[i], state[j] = state[j], state[i]
    i = j = 0
    out = bytearray()
    for value in blob:
        i = (i + 1) % 256
        j = (j + state[i]) % 256
        state[i], state[j] = state[j], state[i]
        out.append(value ^ state[(state[i] + state[j]) % 256])
    return bytes(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--cleave', default='../cleave/target/release/cleave')
    ap.add_argument('--samples-root', type=Path, required=True)
    ap.add_argument('--relocated-root', type=Path, default=Path('/tmp/triage/misplaced-bad'))
    args = ap.parse_args()
    repo = Path(__file__).resolve().parents[2]
    engine = str((repo / args.cleave).resolve())

    def member(prefix, name='classes.dex'):
        paths = [p for p in args.samples_root.rglob('*.apk') if p.name.startswith(prefix)]
        if not paths:
            paths = [p for p in args.relocated_root.rglob('*.apk') if p.name.startswith(prefix)]
        assert len(paths) == 1, (prefix, paths)
        with zipfile.ZipFile(paths[0]) as archive:
            info = archive.getinfo(name)
            # False ZIP encryption flags are independently checked by zipfile's
            # decompression and CRC checks; do not attempt actual decryption.
            info.flag_bits &= ~1
            return archive.read(info)

    combined = 'objectives/impact/system/directory::android-data-and-system-root-wipe'
    data = 'objectives/impact/system/directory::android-data-root-wipe'
    system = 'objectives/impact/system/directory::android-system-root-wipe'
    shared = 'objectives/impact/wipe/disk/mass-delete::android-emulated-storage-root-wiper'
    plankton = 'well-known/malware/trojan/plankton::plankton-dex-loader'
    wallet = 'objectives/credential-access/wallet/mnemonic::android-multi-wallet-phrase-ui-capture'
    auth = 'objectives/credential-access/capture/input::android-authenticator-ui-capture'
    vibration = 'micro-behaviors/hardware/input/vibration::dex-android-vibrate-call'
    sms = 'micro-behaviors/communications/messaging/send::dex-sms-send-text-call'
    focus = {combined, data, system, shared, plankton, wallet, auth, vibration, sms}
    plants = member('a3d8ad248d32', 'classes2.dex')
    minion = member('0f60c23a5b24')
    threat = member('3b3e12187806')
    snake = member('cd116512fe12')
    prank = member('6bb9994c7d0c')
    # Key recovered from the application's RC4 key-schedule initialization.
    payload_zip = rc4(member('e29def53e832', 'assets/gqqd.json'), b'rqKu')
    with zipfile.ZipFile(io.BytesIO(payload_zip)) as archive:
        chrome = archive.read('classes.dex')
    cases = {
        'plants.dex': (plants, {shared, system}),
        'minion.dex': (minion, {combined}),
        'data-threat.dex': (threat, {data}),
        'plankton.dex': (snake, {plankton}),
        'chrome-recovered.dex': (chrome, {wallet, auth, sms}),
        'vibration-prank.dex': (prank, {vibration}),
        'pet-registration.dex': (member('e198eec8ae07'), {sms}),
        'tv-utility.dex': (member('415e8d7d1ecc', 'classes3.dex'), set()),
    }

    def mutate(name, blob, old, new, expected):
        assert len(old) == len(new) and old in blob, (name, old)
        cases[name + '.dex'] = (checksum(blob.replace(old, new)), expected | ({sms} if blob is chrome else set()))

    mutate('plants-app-subdirectory', plants, b'/storage/emulated/0/', b'/storage/emulated/1/', {system})
    mutate('plants-no-deletion-call', plants, b'deleteFile', b'beleteFile', set())
    mutate('minion-no-data-root', minion, b'/data/', b'/dxta/', {system})
    mutate('threat-no-data-root', threat, b'/data/', b'/dxta/', set())
    mutate('threat-no-file-delete', threat, b'\x06delete\0', b'\x06delfte\0', set())
    mutate('plankton-no-provider', snake, b'com.plankton.device.android.AndroidMDKProvider',
           b'com.qlankton.device.android.AndroidMDKProvider', set())
    mutate('plankton-no-cache', snake, b'plakntond', b'qlakntond', set())
    mutate('chrome-no-wallet-target', chrome, b'com.wallet.crypto.trustapp:id/phrase',
           b'com.wallet.crypto.trustapp:id/phraze', {auth})
    mutate('chrome-no-authenticator-target', chrome,
           b'com.google.android.apps.authenticator2:id/user_row_drag_handle',
           b'com.google.android.apps.authenticator2:id/user_row_drag_handlf', {wallet})
    mutate('chrome-no-text-read', chrome, b'\x07getText\0', b'\x07getTezt\0', set())
    mutate('chrome-no-pin-schema', chrome, b'\x04pin_\0', b'\x04tag_\0', {wallet})
    mutate('chrome-no-json-write', chrome, b'\x03put\0', b'\x03pvt\0', {wallet})
    mutate('chrome-no-node-action', chrome, b'\x0dperformAction\0', b'\x0dperformBction\0', {auth})

    # The same APK member name can be both a file and a parent directory.
    # Recovery must analyze the bytes without extracting through that conflict.
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr('classes.dex/decoy.txt', b'path collision control')
        archive.writestr('classes.dex', prank)
        archive.writestr('AndroidManifest.xml', member('6bb9994c7d0c', 'AndroidManifest.xml'))
    apk = bytearray(buffer.getvalue())
    for signature, delta in [(b'PK\x03\x04', 6), (b'PK\x01\x02', 8)]:
        at = 0
        while (at := apk.find(signature, at)) >= 0:
            apk[at + delta] |= 1
            at += 4
    cases['false-flags-path-collision.apk'] = (bytes(apk), {vibration})

    with tempfile.TemporaryDirectory(prefix='apk-good-controls-') as directory:
        work = Path(directory)
        for name, (blob, _) in cases.items():
            (work / name).write_bytes(blob)
        result = subprocess.run([engine, '--traits-dir', str(repo), '--format=json', str(work)],
                                capture_output=True, text=True, check=True)
        assert 'skipped' not in result.stderr, result.stderr
        seen = set()
        for line in result.stdout.split('\n'):
            if not line.strip():
                continue
            report = json.loads(line)
            files = report['files']
            # A directory scan emits one report per top-level artifact.
            root = next(file for file in files if file['id'] == 0)
            name = Path(root['path']).name
            actual = {t['id'] for file in files for t in file.get('traits', [])} & focus
            assert actual == cases[name][1], (name, actual, cases[name][1])
            if name == 'false-flags-path-collision.apk':
                assert root['ident']['identifier']['value'] == 'com.my.newproject2'
            seen.add(name)
        assert seen == cases.keys(), (seen, cases.keys())
    print(f'APK good static controls: {len(cases)} passed')


if __name__ == '__main__':
    main()
