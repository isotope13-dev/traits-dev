#!/usr/bin/env python3
"""Exercise the signed-PE and high-entropy section profile.

Requires clang, lld-link, openssl, osslsigncode and the sibling Cleave release
binary. Creates a temporary self-signed test certificate. PEs are not executed.
"""
from pathlib import Path
import random
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = ROOT.parent / 'cleave/target/release/cleave'
RULE = 'metadata/signed/certificate/signature::signer-verified-pe-high-entropy-data-section'

with tempfile.TemporaryDirectory(prefix='signed-data-entropy-') as temp:
    work = Path(temp)
    rng = random.Random(5421)
    high = ','.join(str(rng.randrange(256)) for _ in range(8192))
    for name, content in (('high', high), ('low', '1')):
        source, obj, pe = (work / (name + ext) for ext in ('.c', '.obj', '.exe'))
        source.write_text('volatile unsigned char data[8192]={' + content +
                          '}; int main(void){return data[0];}\n')
        subprocess.run(['clang', '-target', 'x86_64-pc-windows-msvc', '-c', str(source),
                        '-o', str(obj)], check=True)
        subprocess.run(['lld-link', '/entry:main', '/subsystem:console', '/nodefaultlib',
                        '/out:' + str(pe), str(obj)], check=True)
    key, cert = work / 'key.pem', work / 'cert.pem'
    subprocess.run(['openssl', 'req', '-x509', '-newkey', 'rsa:2048', '-nodes',
                    '-keyout', str(key), '-out', str(cert), '-days', '1',
                    '-subj', '/CN=EntropyFixture'], check=True, capture_output=True)
    for name in ('high', 'low'):
        subprocess.run(['osslsigncode', 'sign', '-certs', str(cert), '-key', str(key),
                        '-in', str(work / (name + '.exe')), '-out',
                        str(work / (name + '-signed.exe'))], check=True, capture_output=True)
    for name, expected in (('high-signed', True), ('high', False), ('low-signed', False)):
        result = subprocess.run([str(CLEAVE), '--traits-dir', str(ROOT), 'test-rules',
                                 '--rules', RULE, str(work / (name + '.exe'))],
                                check=True, capture_output=True, text=True)
        summary = f'Summary: {int(expected)} matched, {int(not expected)} not matched'
        if summary not in result.stdout:
            raise SystemExit(f'{name}: unexpected result\n{result.stdout}\n{result.stderr}')
        print(f'{name}: ok', flush=True)
