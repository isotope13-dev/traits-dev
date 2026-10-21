#!/usr/bin/env python3
"""Compile and scan inert controls; never execute fixture classes or DOS bytes."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('--scratch', required=True)
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
repo = Path(__file__).resolve().parents[3]
neutral = 'micro-behaviors/crypto/cipher::jvm-dpapi-gcm-references'
dos = 'micro-behaviors/fs/write/file/handle::dos-int21-write-saved-vector'
with tempfile.TemporaryDirectory(dir=args.scratch, prefix='acquit-controls-') as directory:
    root = Path(directory)
    stub = root / 'com/sun/jna/platform/win32/Crypt32Util.java'
    stub.parent.mkdir(parents=True)
    stub.write_text('package com.sun.jna.platform.win32; public class Crypt32Util {'
                    'public static byte[] cryptUnprotectData(byte[] b) {return b;}}')
    source = root / 'LocalBackup.java'
    source.write_text('''import javax.crypto.Cipher;
import javax.crypto.spec.GCMParameterSpec;
import javax.crypto.spec.SecretKeySpec;
import com.sun.jna.platform.win32.Crypt32Util;
class LocalBackup {
 static byte[] restore(byte[] wrappedKey, byte[] iv, byte[] ciphertext) throws Exception {
  byte[] key = Crypt32Util.cryptUnprotectData(wrappedKey);
  Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
  cipher.init(Cipher.DECRYPT_MODE, new SecretKeySpec(key, "AES"), new GCMParameterSpec(128, iv));
  return cipher.doFinal(ciphertext);
 }
 static final String DOCUMENTATION = "''' + ('Restore locally encrypted backup. ' * 40) + '''";
}''')
    subprocess.run(['javac', '-g:none', '-d', str(root), str(stub), str(source)], check=True)
    cases = {
        # Real encrypted string-vault bytes at offset 5285; EA is ciphertext.
        'encrypted-resource.bin': bytes.fromhex('b440dfa7cf2118a6bae4fb63a7d97601f77a3c8a39eaa52f103a'),
        # Real DOS write: EA is the ModRM byte in SUB DX,imm16, not a far jump.
        'operand-near-miss.bin': bytes.fromhex('b4408bd581ea3c3281c2323231c9b1c0cd21'),
        'saved-call.bin': bytes.fromhex('b440b902009cff1e0000'),
        'saved-jump.bin': bytes.fromhex('b440ea00000000'),
    }
    for name, data in cases.items():
        (root / name).write_bytes(data + bytes(128))
    paths = [root / 'LocalBackup.class'] + [root / name for name in cases]
    result = subprocess.run([args.cleave, '--traits-dir', str(repo), '--format', 'json',
                             *map(str, paths)], capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(result.stderr + result.stdout)
    remaining = result.stdout.strip()
    files = {}
    while remaining:
        report, end = json.JSONDecoder().raw_decode(remaining)
        remaining = remaining[end:].lstrip()
        for item in report['files']:
            files[Path(item['path']).name] = item
    ids = lambda name: {trait['id'] for trait in files[name].get('traits', [])}
    assert neutral in ids('LocalBackup.class')
    assert not any(t['crit'] >= 4 for t in files['LocalBackup.class'].get('traits', []))
    for name in ['encrypted-resource.bin', 'operand-near-miss.bin']:
        assert dos not in ids(name), name
    for name in ['saved-call.bin', 'saved-jump.bin']:
        assert dos in ids(name), name
print('PASS: local-backup crypto control, two real near misses, two DOS positives')
