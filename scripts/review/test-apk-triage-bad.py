#!/usr/bin/env python3
"""Static APK regressions: argument polarity, root targets and OCR theft legs.

Uses original DEX and equal-length mutations; never loads or executes Android code.
Requires a cleave build linked to filefacts' bounded DEX call extractor.
"""
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


def dex_checksum(blob):
    blob = bytearray(blob)
    blob[12:32] = hashlib.sha1(blob[32:]).digest()
    struct.pack_into('<I', blob, 8, zlib.adler32(blob[12:]) & 0xffffffff)
    return bytes(blob)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--cleave', default='../cleave/target/release/cleave')
    ap.add_argument('--samples-root', type=Path, required=True)
    args = ap.parse_args()
    repo = Path(__file__).resolve().parents[2]
    engine = str((repo / args.cleave).resolve())

    def member(prefix, name):
        paths = [p for p in args.samples_root.rglob('*')
                 if p.is_file() and p.name.startswith(prefix) and p.suffix in {'.apk', '.xapk'}]
        assert len(paths) == 1, (prefix, paths)
        with zipfile.ZipFile(paths[0]) as archive:
            if paths[0].suffix == '.xapk':
                base = next(n for n in archive.namelist() if n.endswith('.apk') and 'config.' not in n)
                with zipfile.ZipFile(io.BytesIO(archive.read(base))) as inner:
                    return inner.read(name)
            return archive.read(name)

    wifi_on = 'micro-behaviors/hardware/wireless/network::android-wifi-enable-dex-call'
    wifi_off = 'micro-behaviors/hardware/wireless/network::android-wifi-disable-dex-call'
    wipe = 'objectives/impact/system/directory::android-data-and-system-root-wipe'
    fields = 'micro-behaviors/communications/http/request/body/multipart::android-photo-ocr-device-upload'
    steal = 'objectives/exfiltration/stealer/credential/value/recovery-secret::android-mnemonic-image-ocr-upload'
    account = 'micro-behaviors/fs/path/credential::android-account-store-path'
    component_on = 'micro-behaviors/os/application/config::dex-component-enable-call'
    component_off = 'micro-behaviors/os/application/config::dex-component-disable-call'
    focus = {wifi_on, wifi_off, wipe, fields, steal, account, component_on, component_off}
    cases = {}

    def case(name, blob, expected):
        cases[name] = (blob, expected)

    qr = member('9228e6cf5457', 'classes2.dex')
    case('wifi-enable.dex', qr, {wifi_on})
    # Independently disassembled WifiManager call at 647630, in utility.q.g.
    # Its preceding const/4 v8,1 is unique in that bounded method region.
    constants = [p for p in range(647312, 647630, 2) if qr[p:p+2] == b'\x12\x18']
    assert len(constants) == 1, constants
    disabled = bytearray(qr)
    disabled[constants[0]+1] = 8  # const/4 v8,0
    case('wifi-disable.dex', dex_checksum(disabled), {wifi_off})
    game = member('5d666a2b3ae5', 'classes3.dex')
    case('renamed-root-wipe.bin', game, {wipe})
    case('no-data-root.dex', dex_checksum(game.replace(b'/data/', b'/dxta/')), set())
    case('no-system-root.dex', dex_checksum(game.replace(b'/sys/', b'/syz/').replace(b'/system/', b'/systen/')), set())
    case('no-delete-helper.dex', dex_checksum(game.replace(b'deleteFile', b'deleteFild')), set())
    wa = member('eba381ace293', 'classes2.dex')
    case('mnemonic-ocr.dex', wa, {fields, steal})
    case('chinese-mnemonic-only.dex', dex_checksum(wa.replace(b'mnemonic', b'nnemonic')), {fields, steal})
    without_terms = wa.replace(b'mnemonic', b'nnemonic').replace('助记词'.encode(), '助记谣'.encode())
    case('no-mnemonic-terms.dex', dex_checksum(without_terms), {fields})
    # Keep both keywords in the DEX pool but replace their two const-string
    # references with the existing empty string. Pool membership is not use.
    strings_count, strings_offset = struct.unpack_from('<II', wa, 56)
    empty_id = None
    for index in range(strings_count):
        offset, = struct.unpack_from('<I', wa, strings_offset + index * 4)
        if wa[offset:offset + 2] == b'\x00\x00':
            empty_id = index
            break
    assert empty_id is not None and empty_id < 65536
    unreferenced = bytearray(wa)
    for instruction in [3691204, 3691210]:
        opcode = unreferenced[instruction]
        assert opcode in {0x1a, 0x1b}
        struct.pack_into('<H' if opcode == 0x1a else '<I', unreferenced, instruction + 2, empty_id)
    case('unused-mnemonic-pool-strings.dex', dex_checksum(unreferenced), {fields})
    case('no-ocr-field.dex', dex_checksum(wa.replace(b'RECOGNIZED_TEXT', b'RECOGNIZED_TEXX')), set())
    case('no-photo-attachment.dex', dex_checksum(wa.replace(b'PHOTO_INFO', b'PHOTO_INFX')), set())
    case('no-text-block-reader.dex', dex_checksum(wa.replace(b'getTextBlocks', b'getTextBlockz')), {fields})
    # Component state 1 enables; a class called Cls is not proof of hiding.
    case('component-enabled.dex', member('bd8c22823fea', 'classes7.dex'), {component_on})
    case('user-directory-prefix.txt', b'/data/system/users/\n', set())
    case('modern-account-database.txt', b'/data/system_ce/0/accounts_ce.db\n', {account})
    case('legacy-account-database.txt', b'/data/system/users/10/accounts.db\n', {account})
    case('fake-dex-api-strings.dex', b'dex\n035\x00' + b'\x00'*104 + b'setWifiEnabled /data/ /system/ deleteFile', set())
    with tempfile.TemporaryDirectory(prefix='apk-triage-controls-') as temporary:
        work = Path(temporary)
        for name, (blob, _) in cases.items():
            (work / name).write_bytes(blob)
        result = subprocess.run([engine, '--traits-dir', str(repo), '--format=json', str(work)],
                                capture_output=True, text=True, check=True)
        assert 'skipped' not in result.stderr, result.stderr
        seen = set()
        for line in result.stdout.split('\n'):
            if not line.strip():
                continue
            for file in json.loads(line)['files']:
                name = Path(file['path']).name
                actual = {t['id'] for t in file.get('traits', [])} & focus
                assert actual == cases[name][1], (name, actual, cases[name][1])
                seen.add(name)
        assert seen == cases.keys(), (seen, cases.keys())
    print(f'APK static controls: {len(cases)} passed')


if __name__ == '__main__':
    main()
