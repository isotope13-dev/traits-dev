"""Offline reference controls; generated PE stubs return immediately.

Usage: python3 check.py SCRATCH_DIRECTORY
No specimen or generated PE is executed. These fixtures test reference
co-occurrence, not execution or binding of registry paths to deletion calls.
"""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location(
    'fixture', ROOT / 'testdata/managed-records-review/verify.py')
fixture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixture)
HOOK = 'objectives/collection/keylog/hook::managed-low-level-hook-file-keylogger'
OLD = 'objectives/collection/keylog/hook::managed-file-keylogger-with-hook'
DELETE = 'micro-behaviors/os/registry/delete::managed-registry-subtree-delete-references'
MEMBER = 'micro-behaviors/os/registry/delete::delete-subkey-tree-member-name'
PATH = 'micro-behaviors/os/registry/keys/policy::safeboot-base-regpath'
RECOVERY = 'objectives/impact/ransom/recovery-inhibition::managed-keylogger-safeboot-delete-references'
KEYS = ['WH_KEYBOARD_LL', 'SetWindowsHookEx', 'UnhookWindowsHookEx',
        'CallNextHookEx', 'keylog', 'AppendAllText']
BASE = r'SYSTEM\CurrentControlSet\Control\SafeBoot'
REG = ['RegistryKey', 'DeleteSubKeyTree', BASE]


def main():
    dest = Path(sys.argv[1])
    dest.mkdir(parents=True, exist_ok=True)
    cases = [
        ('hook-without-polling', KEYS, True, False, False, False),
        ('hook-without-file-records', KEYS[:-1], False, False, False, False),
        ('hook-without-record-label', [m for m in KEYS if m != 'keylog'],
         False, False, False, False),
        ('registry-cleanup', REG, False, True, True, False),
        ('keylogger-recovery-references', KEYS + REG, True, True, True, True),
        ('case-variant-path', KEYS + REG[:-1] + [BASE.lower()],
         True, True, True, True),
        ('other-registry-path', KEYS + REG[:-1] + [r'SOFTWARE\Example'],
         True, True, False, False),
        ('read-only-keylogger', KEYS + ['RegistryKey', BASE],
         True, False, True, False),
        ('wrong-method', KEYS + ['RegistryKey', 'DeleteSubKeyTrees', BASE],
         True, False, True, False),
        ('no-registry-type', KEYS + REG[1:], True, False, True, False),
    ]
    results = []
    for name, markers, hook, delete, path, recovery in cases:
        sample = dest / (name + '.exe')
        sample.write_bytes(fixture.build_pe(markers))
        result = subprocess.run(
            [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
             '--disable', 'third-party', '--format', 'json', str(sample)],
            capture_output=True, text=True, check=True)
        report = json.loads(result.stdout)
        traits = {t['id']: t for f in report['files'] for t in f['traits']}
        expected = {HOOK: hook, DELETE: delete, PATH: path, RECOVERY: recovery,
                    OLD: False}
        actual = {id: id in traits for id in expected}
        assert actual == expected, (name, actual, expected, result.stderr)
        for id in [DELETE, MEMBER, PATH]:
            if id in traits:
                assert traits[id]['crit'] == 3, (name, id, traits[id])
        if name == 'registry-cleanup':
            assert not any(t['crit'] >= 4 for t in traits.values()), traits
        results.append({'case': name, 'expected': expected, 'actual': actual})
        print('PASS', name, flush=True)
    (dest / 'results.json').write_text(json.dumps(results, indent=2) + '\n')


if __name__ == '__main__':
    main()
