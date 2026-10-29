#!/usr/bin/env python3
"""Check signed PE checksum/extra-byte observations and their time boundary.

Requires clang, lld-link, openssl, osslsigncode and the sibling Cleave release
binary. Temporary test keys and PEs are created for analysis, never execution.
"""
from pathlib import Path
import struct
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = ROOT.parent / 'cleave/target/release/cleave'
PROFILE = 'metadata/signed/certificate/signature::signer-checksum-mismatch-unclaimed-bytes'
INTEGRITY = 'metadata/signed/certificate/signature::pe-signature-verified'

with tempfile.TemporaryDirectory(prefix='signed-extra-bytes-') as temp:
    work = Path(temp)
    source, obj, unsigned = (work / n for n in ('main.c', 'main.obj', 'unsigned.exe'))
    source.write_text('volatile unsigned char data[70000]={1}; '
                      'int main(void){return data[0];}\n')
    subprocess.run(['clang', '-target', 'x86_64-pc-windows-msvc', '-c', str(source),
                    '-o', str(obj)], check=True)
    subprocess.run(['lld-link', '/entry:main', '/subsystem:console', '/nodefaultlib',
                    '/out:' + str(unsigned), str(obj)], check=True)
    key, cert = work / 'key.pem', work / 'cert.pem'
    subprocess.run(['openssl', 'req', '-x509', '-newkey', 'rsa:2048', '-nodes',
                    '-keyout', str(key), '-out', str(cert), '-days', '1',
                    '-subj', '/CN=OverlayFixture'], check=True, capture_output=True)
    presign = work / 'presign.exe'
    presign.write_bytes(unsigned.read_bytes() + b'P' * 1024)
    for source_file, name in ((unsigned, 'signed'), (presign, 'presign-signed')):
        subprocess.run(['osslsigncode', 'sign', '-certs', str(cert), '-key', str(key),
                        '-in', str(source_file), '-out', str(work / (name + '.exe'))],
                       check=True, capture_output=True)
    (work / 'postsign-extra.exe').write_bytes((work / 'signed.exe').read_bytes() + b'Z' * 1024)
    (work / 'unsigned-extra.exe').write_bytes(presign.read_bytes())
    presign_data = bytearray((work / 'presign-signed.exe').read_bytes())
    checksum_offset = struct.unpack_from('<I', presign_data, 60)[0] + 24 + 64
    struct.pack_into('<I', presign_data, checksum_offset, 1)
    (work / 'presign-stale.exe').write_bytes(presign_data)
    for name, expected in (('presign-stale', True), ('postsign-extra', True),
                           ('signed', False), ('unsigned-extra', False)):
        result = subprocess.run([str(CLEAVE), '--traits-dir', str(ROOT), 'test-rules',
                                 '--rules', PROFILE + ',' + INTEGRITY,
                                 str(work / (name + '.exe'))], check=True,
                                capture_output=True, text=True)
        status = 'MATCHED ' if expected else 'NOT MATCHED '
        if '\n' + status + PROFILE + ' ' not in result.stdout:
            raise SystemExit(f'{name}: wrong profile result\n{result.stdout}\n{result.stderr}')
        if name == 'presign-stale' and '\nMATCHED ' + INTEGRITY + ' ' not in result.stdout:
            raise SystemExit(f'{name}: signed image is not intact\n{result.stdout}')
        print(f'{name}: ok', flush=True)
