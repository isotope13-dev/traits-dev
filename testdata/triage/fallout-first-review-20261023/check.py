"""Static controls for the reviewed RATs; never execute a specimen.

Supply --native (the AutoIt carrier), --managed, --runtime (official AutoIt3),
and --work-dir. Uses atomscan's embedded engine, with local traits explicitly
selected, so the same analysis engine is used for before/after comparisons.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
KEYLOG = 'objectives/collection/keylog/device::native-translated-scrambled-key-log'
CLEANUP = 'objectives/evasion/self-delete/file/script::native-keylogger-batch-self-cleanup'
DELETE = 'micro-behaviors/fs/delete/file/self::batch-self-delete'
BOOT = 'objectives/persistence/system/registry/session-manager::managed-keylogger-bootexecute-references'
MANAGED = 'objectives/collection/keylog/hook::dotnet-hook-keylog-recording'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ['native', 'managed', 'runtime', 'work-dir']:
        parser.add_argument('--'+name, type=Path, required=True)
    args = parser.parse_args()
    args.work_dir.mkdir(parents=True, exist_ok=True)
    native, managed = args.native.read_bytes(), args.managed.read_bytes()
    assert hashlib.sha256(native).hexdigest() == '642b1c6ae22b17bef3300c1a3e232f359072fb7d424e34cf0f4866f644c8fda2'
    assert hashlib.sha256(managed).hexdigest() == '389915f932efa1ea6e3385dec2ab35dc388ffa24bd5b38d494f5cc973423b7ea'
    payload = native[0x1056d4:0x1056d4+135168]
    assert payload[:2] == b'MZ'
    before = b'del "%%~f0"'
    assert before in payload
    boot = 'BootExecute'.encode('utf-16le')
    assert boot in managed
    cases = [
        ('netwire.exe', payload, {KEYLOG, CLEANUP, DELETE}, set()),
        ('netwire-other-target.exe', payload.replace(before, b'del "%%~f1"'),
         {KEYLOG}, {CLEANUP, DELETE}),
        ('managed.exe', managed, {MANAGED, BOOT}, set()),
        ('managed-other-value.exe', managed.replace(boot, 'BootExecutx'.encode('utf-16le')),
         {MANAGED}, {BOOT}),
        ('ordinary-cleanup.bat', b'@echo off\r\ndel "%~f0"\r\n', {DELETE}, {CLEANUP, BOOT}),
        ('other-target.bat', b'@echo off\r\ndel "%~f1"\r\n', set(), {DELETE, CLEANUP, BOOT}),
        ('official-AutoIt3.exe', args.runtime.read_bytes(), set(), {KEYLOG, CLEANUP, BOOT}),
    ]

    def scan(case):
        name, data, present, absent = case
        path = args.work_dir/name
        path.write_bytes(data)
        env = {**os.environ, 'CLEAVE_TRAITS_DIR': str(ROOT)}
        result = subprocess.run(['atomscan', '--no-update', '--mode', 'slow',
                                 '--follow=none', '-f', 'json', str(path)],
                                capture_output=True, text=True, env=env, cwd=ROOT)
        (args.work_dir/(name+'.json')).write_text(result.stdout)
        (args.work_dir/(name+'.log')).write_text(result.stderr)
        report = json.loads(result.stdout)
        traits = {t['id'] for f in report['raw']['files'] for t in f['traits']}
        return {'case': name, 'missing': sorted(present-traits),
                'unexpected': sorted(absent & traits)}

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(scan, cases))
    (args.work_dir/'results.json').write_text(json.dumps(results, indent=2)+'\n')
    print(json.dumps(results, indent=2))
    assert all(not r['missing'] and not r['unexpected'] for r in results)


if __name__ == '__main__':
    main()
