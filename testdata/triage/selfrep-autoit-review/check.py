#!/usr/bin/env python3
"""Exercise original bytes, same-length PE ablations and benign shell controls.

Usage: python3 check.py --samples-root /path/to/samples --cleave /path/to/cleave
No specimen is executed or saved into the repository.
"""
import argparse
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
HTTP = 'objectives/command-and-control/botnet/loader::repeated-http-selfrep-loader'
FTP = 'objectives/command-and-control/botnet/loader::repeated-ftp-selfrep-loader'
EXEC = 'objectives/execution/payload/file-exec::raw-ip-bulk-download-chmod-exec'
CLEAN = 'objectives/evasion/indicator-removal/cleanup::ftp-selfrep-loader-payload-cleanup'
RUNPE = 'objectives/execution/payload/process-inject::autoit-serialized-framework-runpe'
START = 'objectives/persistence/login/registry/run-key::autoit-runpe-hidden-startup-config'
MASQ = 'objectives/evasion/masquerade/version-resource/claim::autoit-scite-version-masquerade'
SH = 'micro-behaviors/process/create/shell/target::shell-exec-script-path'
PERM = 'micro-behaviors/fs/chmod/executable/dangerous::busybox-chmod-plus-x'
RESOURCE = 'metadata/binary/resource/entropy::autoit-high-entropy-resource-section'
MAGIC = b'@NetsealIsTheBestLicensingSystemEverCreated@'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--samples-root', type=Path, required=True)
    ap.add_argument('--cleave', default=os.environ.get('CLEAVE', 'cleave'))
    args = ap.parse_args()
    http = (args.samples_root / 'e06be431a8d4/wget.sh').read_bytes()
    ftp = (args.samples_root / '823efb0d0247/823efb0d0247dd4d178f07e6ac7a564697ddac95036f311ef1beabd5f4cfd71e').read_bytes()
    pe = (args.samples_root / '08bd1e2347fc/2026-10-15_3b980852966023d40ad9c5a29bea7e03_elex_stop').read_bytes()
    cases = []

    def case(name, data, present=(), absent=(), benign=False):
        cases.append((name, data, set(present), set(absent), benign))

    case('renamed-http.sh', http, [HTTP, EXEC, PERM], [SH])
    case('renamed-ftp.sh', ftp, [FTP, CLEAN, PERM], [SH])
    case('http-installer.sh', http.replace(b'selfrep', b'--version'), [PERM], [HTTP, EXEC, SH], True)
    case('ftp-installer.sh', ftp.replace(b'selfrep', b'--version'), [PERM], [FTP, CLEAN, SH], True)
    case('renamed-payloads.sh', http.replace(b'jkl', b'new').replace(b'185.228.72.128', b'91.200.12.34'), [HTTP, EXEC])
    case('shebang-only.sh', b'#!/bin/sh\necho ready\n', [], [SH], True)
    case('shell-path.sh', b'#!/bin/sh\nsh ./helper.sh\n', [SH], [], True)
    case('absolute-shell.sh', b'#!/bin/sh\n/bin/bash ./helper.sh\n', [SH], [], True)
    case('sudo-shell.sh', b'#!/bin/sh\necho ready; sudo sh ./helper.sh\n', [SH], [], True)
    case('positive.exe', pe, [RUNPE, START, MASQ, RESOURCE])
    case('no-payload-field.exe', pe.replace(MAGIC + b'0x', MAGIC + b'zz'), [MASQ], [RUNPE, START])
    case('no-host-field.exe', pe.replace(b'Microsoft.NET', b'Microsoft.NEX'), [MASQ], [RUNPE, START])
    case('alternate-drive.exe', pe.replace(MAGIC + b'C:', MAGIC + b'D:'), [RUNPE, START])
    flags = MAGIC + b'2' + MAGIC + b'1' + MAGIC
    case('startup-disabled.exe', pe.replace(flags, MAGIC + b'0' + MAGIC + b'0' + MAGIC), [RUNPE], [START])
    case('different-version-claims.exe', pe.replace('SciTE'.encode('utf-16le'), 'Other'.encode('utf-16le')), [RUNPE, START], [MASQ])
    runtime = bytearray(pe)
    runtime[0x92400:0xd0400] = bytes(0x3e000)
    runtime[0x92700:0x92708] = b'AU3!EA06'
    case('runtime-api-control.exe', bytes(runtime), [], [RUNPE, START, MASQ], True)

    def scan(c, temp):
        name, data, present, absent, benign = c
        path = temp / name
        path.write_bytes(data)
        proc = subprocess.run([args.cleave, '--traits-dir', str(ROOT), '--json', str(path)],
                              cwd=ROOT, capture_output=True, text=True, check=True)
        report = json.loads(proc.stdout)
        traits = report['files'][0]['traits']
        ids = {t['id'] for t in traits}
        assert present <= ids, (name, 'missing', sorted(present - ids))
        assert not absent & ids, (name, 'unexpected', sorted(absent & ids))
        if benign:
            assert not any(t['crit'] >= 4 for t in traits), (name, 'nonbenign', [t['id'] for t in traits if t['crit'] >= 4])
        return name

    with tempfile.TemporaryDirectory(prefix='selfrep-autoit-') as temp:
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
            futures = [pool.submit(scan, c, Path(temp)) for c in cases]
            failures = []
            for future in futures:
                try:
                    print('PASS', future.result(), flush=True)
                except Exception as exc:
                    failures.append(str(exc))
                    print('FAIL', exc, flush=True)
            assert not failures, failures
    print(f'{len(cases)} focused controls passed')


if __name__ == '__main__':
    main()
