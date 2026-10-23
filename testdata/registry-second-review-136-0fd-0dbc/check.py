#!/usr/bin/env python3
"""Static regression checks; no specimen or recovered payload is executed."""
import argparse
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
FIX = Path(__file__).resolve().parent
SHC = 'metadata/lang/compiler/native::shc-script-wrapper'
CRYPT = 'objectives/anti-static/obfuscation/payload/encoded/exec::shc-encrypted-script-launcher'
PAD = 'objectives/evasion/process/hidden/argv-env::shc-script-argument-padding'
KEY = 'micro-behaviors/crypto/kdf/file::rc4-wrapper-file-keying-support'
ACL = 'micro-behaviors/os/security/descriptor::acl-world-access-references'
OLD = {
    'third_party/SigBase/EXT/SUSP/OBFUSC/Macos/Roothelper/Obfuscated',
    'objectives/anti-static/obfuscation/binary-metrics/shape::macho-encrypted-payload-launcher',
    'objectives/anti-static/obfuscation/binary-metrics/shape::macho-environmentally-keyed-payload',
    'objectives/privilege-escalation/exploit/race-condition::oplock-reparse-disposition-race',
    'micro-behaviors/os/security/descriptor::world-writable-acl-setup',
}

def documents(text):
    decoder = json.JSONDecoder()
    index = 0
    while text[index:].strip():
        while text[index].isspace():
            index += 1
        value, index = decoder.raw_decode(text, index)
        yield value


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cleave', default='cleave')
    parser.add_argument('--samples-root', type=Path)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    targets = [str(FIX / name) for name in (
        'benign-shc.macho', 'benign-shc-no-padding.macho',
        'unrelated-rc4-exec.macho', 'oplock-only.cpp',
        'unused-world-authority.cpp', 'cloud-provider.cpp',
        'recovered-installer.sh', 'filesystem-swap.cpp', 'race-without-image-write.cpp',
    )]
    if args.samples_root:
        targets += [str(args.samples_root / 'samples/1360718b000d/remediation_race.cpp'),
                    str(args.samples_root / 'samples/0fd28c0d63f8/defender_hydration_path_confusion.cpp'),
                    str(args.samples_root / 'extract/0dbc87/ba14cfe19a51a168813ee1d2bd2e57a8d2aeffa7721575772b6718114df778f3.macho')]
    result = subprocess.run([args.cleave, '--traits-dir', str(ROOT), '--format', 'json', *targets],
                            capture_output=True, text=True, check=True,
                            env={**os.environ, 'CLEAVE_VALIDATE': '0'})
    records = []
    for doc in documents(result.stdout):
        for file in doc.get('files', []):
            name = Path(file['path']).name
            traits = {t['id']: t['crit'] for t in file.get('traits', [])}
            assert not OLD.intersection(traits), (name, OLD.intersection(traits))
            if name.startswith('benign-shc'):
                assert traits[SHC] == 3 and traits[CRYPT] == 4 and traits[KEY] == 3, name
                assert (PAD in traits) == (name == 'benign-shc.macho'), name
                assert 5 not in traits.values(), name
            elif name == 'unrelated-rc4-exec.macho':
                assert SHC not in traits and CRYPT not in traits and PAD not in traits, name
                assert 'micro-behaviors/crypto/symmetric/stream/rc4::arc4-routine-symbol' in traits
                assert 'micro-behaviors/process/create/exec::c-exec-variants' in traits
                assert 5 not in traits.values(), name
            elif name == 'oplock-only.cpp':
                assert traits['micro-behaviors/fs/file/oplock::oplock-synchronization'] == 3
                assert all(v < 4 for v in traits.values()), name
            elif name in ('filesystem-swap.cpp', 'race-without-image-write.cpp'):
                assert traits['micro-behaviors/fs/link/junction::oplock-disposition-reparse-apis'] == 3
                assert all(v < 4 for v in traits.values()), name
            elif name == 'unused-world-authority.cpp':
                assert traits[ACL] == 3
                assert all(v < 4 for v in traits.values()), name
            elif name == 'cloud-provider.cpp':
                assert 'micro-behaviors/fs/sync/cloud-files::sync-root-provider-hydration' in traits
                assert all(v < 4 for v in traits.values()), name
            elif name == 'recovered-installer.sh':
                assert traits['objectives/evasion/masquerade/identity/service::user-launchagent-apple-label-masquerade'] == 5
            elif name == 'remediation_race.cpp':
                assert traits['objectives/privilege-escalation/exploit/race-condition::transacted-system32-image-write-race'] == 5
                assert traits['objectives/privilege-escalation/exploit/race-condition::task-run-with-system32-write-race'] == 5
                assert traits['micro-behaviors/fs/link/junction::oplock-disposition-reparse-apis'] == 3
            elif name == 'defender_hydration_path_confusion.cpp':
                assert traits[ACL] == 3
                assert sum(v == 5 for v in traits.values()) == 4
            else:
                assert traits[CRYPT] == 4 and traits[PAD] == 4 and traits[KEY] == 3
                assert 5 not in traits.values(), name
            records.append({'file': name, 'hostile': [k for k,v in traits.items() if v == 5],
                            'suspicious': [k for k,v in traits.items() if v == 4]})
    assert len(records) == len(targets), (len(records), len(targets))
    if args.report:
        args.report.write_text(json.dumps(records, indent=2) + '\n')
    print(f'{len(records)} static regression checks passed')

if __name__ == '__main__':
    main()
