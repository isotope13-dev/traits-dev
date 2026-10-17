"""Check classification boundaries using inert PE byte mutations.

Usage: python3 check.py EUPDATE_UNPACKED STORM_LOADER --out SCRATCH_DIR
No specimen or generated control is executed.
"""
import argparse
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
PROXY = 'objectives/command-and-control/channel/proxy::hash-rotating-port-seizing-proxy'
ROTATE = 'micro-behaviors/fs/write/file/executable::self-hash-rotation-relaunch'
RUN = 'micro-behaviors/os/autorun/login-items::native-standby-self-mutation-run-key'
LANMAN = 'objectives/persistence/system/service/loader::lanmanserver-resource-injection-hijack'
FALLBACK = 'objectives/persistence/system/service/loader::lanmanserver-servicedll-remote-injection'
ACTIVE = 'objectives/persistence/login/registry/autostart::active-setup-service-dll-injector'
CLEANUP = 'objectives/evasion/self-delete/process::native-dll-injector-shell-cleanup'
FAMILY = 'well-known/malware/botnet/stormattack::stormattack-service-dll-injector'
HANDOFF = 'micro-behaviors/process/inject/dll::x86-remote-dll-export-thread'
LOADER = {LANMAN, ACTIVE, CLEANUP, FAMILY, HANDOFF}


def replace(data, old, new):
    assert len(old) == len(new)
    assert old in data, old
    return data.replace(old, new)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('eupdate', type=Path)
    parser.add_argument('storm', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--cleave', default='cleave')
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    eupdate, storm = args.eupdate.read_bytes(), args.storm.read_bytes()
    wide = lambda text: text.encode('utf-16le')
    renamed = replace(eupdate, wide('Eupdate Helper'), wide('Generic Mirror'))
    renamed = replace(renamed, wide('EupdateHelper'), wide('GenericHelper'))
    renamed = replace(renamed, b'#HS:', b'#ID:')
    no_rotation = replace(eupdate, wide('mutate: hash changed'), wide('mutate: file changed'))
    no_handoff = bytearray(storm)
    # The resolved export in EAX is no longer the remote thread's entry.
    assert no_handoff[0x1236:0x123a] == bytes.fromhex('56 50 6a 00')
    no_handoff[0x1237] = 0x52  # PUSH EDX instead of PUSH EAX
    no_crt = replace(storm, b'fread\0', b'freax\0')
    no_write = replace(storm, b'RegSetValueExA\0', b'RexSetValueExA\0')
    cases = [
        ('mirror', eupdate, {ROTATE, RUN}, {PROXY}, True),
        ('mirror-no-product-identity', renamed, {ROTATE, RUN}, {PROXY}, True),
        ('mirror-no-rotation-diagnostic', no_rotation, set(), {PROXY, ROTATE, RUN}, True),
        ('loader', storm, LOADER, {FALLBACK}, False),
        ('loader-no-export-handoff', bytes(no_handoff), set(), LOADER | {FALLBACK}, False),
        ('loader-no-crt-read', no_crt, LOADER - {ACTIVE}, {ACTIVE}, False),
        ('loader-no-registry-write', no_write, {CLEANUP, HANDOFF}, {LANMAN, FALLBACK, ACTIVE, FAMILY}, False),
    ]
    results = []
    env = {**os.environ, 'RAYON_NUM_THREADS': '2'}
    env.pop('CLEAVE_VALIDATE', None)
    for name, data, present, absent, benign in cases:
        path = args.out / (name + '.exe')
        path.write_bytes(data)
        result = subprocess.run(
            [args.cleave, '--traits-dir', str(ROOT), '--format', 'json', str(path)],
            capture_output=True, text=True, check=True, env=env, timeout=300)
        report = json.loads(result.stdout)
        traits = report['files'][0]['traits']
        ids = {t['id'] for t in traits}
        assert present <= ids, (name, 'missing', present - ids)
        assert not absent & ids, (name, 'unexpected', absent & ids)
        if benign:
            assert not [t for t in traits if t['crit'] == 5], name
            assert len([t for t in traits if t['crit'] == 4]) <= 1, name
        results.append({'case': name, 'passed': True,
                        'required_present': sorted(present), 'required_absent': sorted(absent)})
    (args.out / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
    print(f'Passed {len(results)} controls')


if __name__ == '__main__':
    main()
