#!/usr/bin/env python3
"""Static regression controls; never execute the reconstructed Windows code."""
import argparse
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
TOKEN = 'objectives/credential-access/discord/token::discord-stored-token-cng-decryption'
QUERY = 'objectives/credential-access/discord/token::native-stored-token-account-query'
LOGON = 'objectives/persistence/login/registry/script::native-userinit-mpr-value-write'
PYLOGON = 'objectives/persistence/login/registry/script::winreg-userinit-mpr-value-write'
HIVE = 'objectives/persistence/login/registry/run-key::default-user-hive-run-key-modification'
LOAD = 'micro-behaviors/os/registry/offline-hive::default-user-hive-load'
MODE = 'micro-behaviors/crypto/cipher::bcrypt-chaining-mode-gcm'
PREFIX = 'micro-behaviors/data/format/credentials::discord-encrypted-token-prefix-source'


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--cleave', default='cleave')
    p.add_argument('--fixtures-dir', type=Path, required=True)
    p.add_argument('--report', type=Path)
    args = p.parse_args()
    args.fixtures_dir.mkdir(parents=True, exist_ok=True)
    original = (HERE / 'native-reconstruction.cpp').read_text()
    new_objectives = [TOKEN, QUERY, LOGON, PYLOGON, HIVE]
    cases = []

    def add(name, source, yes=(), no=()):
        target = args.fixtures_dir / name
        target.write_text(source)
        cases.append((target, list(yes), list(no)))

    add('native-reconstruction.cpp', original, [TOKEN, QUERY, LOGON, HIVE, LOAD])
    # The names of payloads, registry values, and mounts are operator choices.
    renamed = original.replace('Windows Update', 'Session Helper').replace('ProfileSeed', 'NewMount')
    renamed = renamed.replace('svchost.exe', 'worker.exe').replace('logon.cmd', 'resume.cmd')
    add('renamed.cpp', renamed, [TOKEN, QUERY, LOGON, HIVE])
    for suffix, before, after in [
        ('wrong-store', r'discord\\Local Storage', r'editor\\Local Storage'),
        ('wrong-record', 'dQw4w9WgXcQ:', 'unrelated-record:'),
        ('cbc', 'ChainingModeGCM', 'ChainingModeCBC'),
        ('encryption', 'BCryptDecrypt', 'BCryptEncrypt'),
    ]:
        add(suffix + '.cpp', original.replace(before, after), no=[TOKEN])
    add('other-profile.cpp', original.replace(r'Users\\Default', r'Users\\Alice'),
        [TOKEN, LOGON], [LOAD, HIVE])
    add('registry-read.cpp', '''
#include <windows.h>
void read(HKEY h, BYTE *p, DWORD *n) {
    RegQueryValueExW(h, L"UserInitMprLogonScript", 0, 0, p, n);
}
''', no=[LOGON, HIVE])
    add('default-profile-read.cpp', r'''
#include <windows.h>
void read() {
    RegLoadKeyA(HKEY_USERS, "Template", "D:\\Users\\Default\\NTUSER.DAT");
    RegUnLoadKeyA(HKEY_USERS, "Template");
}
''', ['micro-behaviors/os/registry/offline-hive::native-load-default-user-hive'], [LOGON, HIVE])
    add('comments.cpp', '/*\n' + original + '\n*/\nint main() {return 0;}\n', no=new_objectives)
    add('own-secret.cpp', '''
#include <bcrypt.h>
void decrypt(BCRYPT_KEY_HANDLE key, unsigned char *buffer) {
    BCRYPT_ALG_HANDLE alg;
    BCryptOpenAlgorithmProvider(&alg, L"AES", 0, 0);
    BCryptSetProperty(alg, L"ChainingMode", (PUCHAR)L"ChainingModeGCM", 32, 0);
    BCryptGenerateSymmetricKey(alg, &key, 0, 0, buffer, 32, 0);
    BCryptDecrypt(key, buffer, 32, 0, 0, 0, buffer, 32, 0, 0);
}
''', [MODE], no=new_objectives)
    add('ordinary-api-client.cpp', '''
#include <winhttp.h>
void query(HINTERNET s) {
    auto c = WinHttpConnect(s, L"discord.com", 443, 0);
    auto r = WinHttpOpenRequest(c, L"GET", L"/api/v10/users/@me", 0, 0, 0, 0);
    WinHttpSendRequest(r, 0, 0, 0, 0, 0, 0);
    WinHttpQueryHeaders(r, 0, 0, 0, 0, 0);
}
''', no=new_objectives)
    add('persistence.py', r'''
import winreg

def install(script, image):
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_SET_VALUE) as k:
        winreg.SetValueEx(k, "UserInitMprLogonScript", 0, winreg.REG_SZ, script)
    winreg.LoadKey(winreg.HKEY_USERS, "NewTemplate", r"D:\Users\Default\NTUSER.DAT")
    try:
        with winreg.OpenKey(winreg.HKEY_USERS, r"NewTemplate\Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE) as k:
            winreg.SetValueEx(k, "Session Agent", 0, winreg.REG_EXPAND_SZ, image)
    finally:
        winreg.UnloadKey(winreg.HKEY_USERS, "NewTemplate")
''', [PYLOGON, HIVE, LOAD])
    add('other-hive.py', r"""
import winreg
winreg.LoadKey(winreg.HKEY_USERS, "Saved", r"D:\Backups\NTUSER.DAT")
with winreg.OpenKey(winreg.HKEY_USERS, r"Saved\Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE) as k:
    winreg.SetValueEx(k, "Agent", 0, winreg.REG_SZ, "worker.exe")
""", no=[LOAD, HIVE])
    add('hive-name-is-not-path.cpp', r"""
#include <windows.h>
void load() {
    RegLoadKeyA(HKEY_USERS, "C:\\Users\\Default\\NTUSER.DAT", "D:\\Backup\\NTUSER.DAT");
}
""", no=[LOAD, HIVE])
    add('mixed-value-case.cpp', original.replace('UserInitMprLogonScript', 'USERINITMPRLOGONSCRIPT'), [LOGON])
    add('prefix.py', 'prefix = "dQw4w9WgXcQ:"\n', [PREFIX], no=new_objectives)
    add('prefix.rs', 'const PREFIX: &str = "dQw4w9WgXcQ:";\n', [PREFIX], no=new_objectives)
    add('prefix.cs', 'class Record { const string Prefix = "dQw4w9WgXcQ:"; }\n', [PREFIX], no=new_objectives)
    add('ctypes-gcm.py', r'''
import ctypes
from pathlib import Path

bcrypt = ctypes.WinDLL("bcrypt.dll")
store = Path("discord\\Local Storage\\leveldb")
prefix = "dQw4w9WgXcQ:"

def recover(alg, key, secret, record, info, result, written):
    bcrypt.BCryptOpenAlgorithmProvider(ctypes.byref(alg), "AES", None, 0)
    bcrypt.BCryptSetProperty(alg, "ChainingMode", "ChainingModeGCM", 32, 0)
    bcrypt.BCryptGenerateSymmetricKey(alg, ctypes.byref(key), None, 0, secret, 32, 0)
    return bcrypt.BCryptDecrypt(key, record, len(record), info, None, 0, result, len(result), written, 0)
''', [TOKEN, PREFIX, MODE])

    result = subprocess.run([args.cleave, '--traits-dir', str(REPO), '--format', 'json',
                             'analyze', str(args.fixtures_dir)], text=True, capture_output=True)
    if result.returncode:
        raise SystemExit(result.stderr)
    reports = []
    decoder = json.JSONDecoder()
    remaining = result.stdout.lstrip()
    while remaining:
        report, end = decoder.raw_decode(remaining)
        reports.append(report)
        remaining = remaining[end:].lstrip()
    actual = {Path(f['path']).name: {t['id'] for t in f.get('traits', [])}
              for report in reports for f in report['files']}
    outcomes = []
    for target, yes, no in cases:
        ids = actual.get(target.name, set())
        missing = sorted(set(yes) - ids)
        unexpected = sorted(set(no) & ids)
        outcomes.append(dict(file=target.name, missing=missing, unexpected=unexpected,
                             passed=not missing and not unexpected))
    if args.report:
        args.report.write_text(json.dumps(outcomes, indent=2) + '\n')
    failed = [x for x in outcomes if not x['passed']]
    if failed:
        print(json.dumps(failed, indent=2))
        return 1
    print(f'{len(outcomes)} static cases passed')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
