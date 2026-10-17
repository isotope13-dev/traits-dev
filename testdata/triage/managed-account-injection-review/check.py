"""Static PE evidence controls. Generated images return immediately; never run them.

Usage: python3 check.py <scratch-directory>
"""
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
build_pe = runpy.run_path(str(ROOT / 'testdata/managed-records-review/verify.py'))['build_pe']
KEYS = ['Append', 'WH_KEYBOARD_LL', 'SetWindowsHookEx', 'UnhookWindowsHookEx',
        'CallNextHookEx', 'Keylogger', 'KEYLOG:']
LAUNCH = ['ProcessStartInfo', 'set_CreateNoWindow', 'set_UseShellExecute']
ACCOUNT = ['user arbitrary_account arbitrary_password /add',
           'localgroup administrators arbitrary_account /add']
INJECT = ['CreateProcess', 'CREATE_SUSPENDED', 'ZwUnmapViewOfSection',
          'VirtualAllocEx', 'WriteProcessMemory', 'GetThreadContext',
          'SetThreadContext', 'ResumeThread']
USER = 'micro-behaviors/os/user/account::net-user-create-password-arguments'
ADMIN = 'micro-behaviors/os/group/membership::net-local-admin-add-arguments'
BACKDOOR = 'objectives/persistence/login/account/create::managed-keylogger-admin-account-arguments'
PROFILE = 'micro-behaviors/process/inject/runtime/thread-context::dotnet-suspended-injection-api-set'
OLD = 'objectives/evasion/process/injection/hollowing/process::dotnet-process-hollowing'


def main():
    dest = Path(sys.argv[1])
    dest.mkdir(parents=True, exist_ok=True)
    cases = [
        ('provisioning-only', LAUNCH + ACCOUNT, True, True, False, False),
        ('keylogger-admin-arguments', KEYS + LAUNCH + ACCOUNT, True, True, True, False),
        ('keylogger-no-admin-arguments', KEYS + LAUNCH + ACCOUNT[:1], True, False, False, False),
        ('keylogger-no-create-arguments', KEYS + LAUNCH + ACCOUNT[1:], False, True, False, False),
        ('interactive-password', LAUNCH + ['user test * /add'], False, False, False, False),
        ('option-without-password', LAUNCH + ['user test /domain /add'], False, False, False, False),
        ('query-user', LAUNCH + ['user test', 'localgroup administrators'], False, False, False, False),
        ('managed-injection-api-catalog', INJECT, False, False, False, True),
        ('missing-thread-set', [x for x in INJECT if x != 'SetThreadContext'], False, False, False, False),
    ]

    def check(case):
        name, markers, user, admin, backdoor, profile = case
        path = dest / (name + '.exe')
        path.write_bytes(build_pe(markers))
        result = subprocess.run(
            [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
             '--disable', 'third-party', '--format', 'json', str(path)],
            capture_output=True, text=True, check=True)
        report = json.loads(result.stdout)
        traits = {t['id']: t for f in report['files'] for t in f['traits']}
        for trait, expected in [(USER, user), (ADMIN, admin), (BACKDOOR, backdoor), (PROFILE, profile)]:
            assert (trait in traits) == expected, (name, trait, sorted(traits))
        assert OLD not in traits, name
        if not any(x in KEYS for x in markers):
            assert not any(t['crit'] == 5 for t in traits.values()), name
        if profile:
            assert traits[PROFILE]['crit'] == 4, name
        print('PASS', name, flush=True)

    with ThreadPoolExecutor(max_workers=3) as pool:
        list(pool.map(check, cases))


if __name__ == '__main__':
    main()
