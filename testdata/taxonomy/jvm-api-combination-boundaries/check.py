#!/usr/bin/env python3
"""API co-occurrence must not convict benign JVM database maintenance."""
import json
import pathlib
import subprocess
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[3]


def analyze(path):
    raw = subprocess.check_output(
        ['cleave', '--traits-dir', str(ROOT), '--format', 'json', str(path)], text=True)
    return json.loads(raw)['files']


with tempfile.TemporaryDirectory(prefix='jvm-api-controls-') as tmp:
    tmp = pathlib.Path(tmp)
    sources = {
        'com/sun/jna/platform/win32/Crypt32Util.java': '''
package com.sun.jna.platform.win32;
public class Crypt32Util {
    public static byte[] cryptUnprotectData(byte[] value) { return value; }
}''',
        'com/google/gson/JsonParser.java': '''
package com.google.gson;
public class JsonParser {}''',
        'ProtectedDatabaseMaintenance.java': '''
import javax.crypto.Cipher;
import javax.crypto.spec.*;
import java.sql.DriverManager;
import java.util.Base64;
import com.google.gson.JsonParser;
import com.sun.jna.platform.win32.Crypt32Util;
public class ProtectedDatabaseMaintenance {
    // Compiled for static analysis, never executed. These are also ordinary
    // database backup / key-migration APIs, not evidence of browser theft.
    public byte[] migrate(byte[] data, String database) throws Exception {
        new ProcessBuilder("sqlite3", database, ".backup copy.db").start().waitFor();
        DriverManager.getConnection("jdbc:sqlite:" + database).close();
        byte[] key = Crypt32Util.cryptUnprotectData(Base64.getDecoder().decode(data));
        new SecretKeySpec(key, "AES");
        new GCMParameterSpec(128, data);
        new DESedeKeySpec(data);
        new JsonParser();
        System.getenv("APPDATA");
        return Cipher.getInstance("AES/GCM/NoPadding").doFinal(data);
    }
    public String xor(char[] chars, int key) {
        for (int i = 0; i < chars.length; i++) chars[i] ^= key;
        return new String(chars);
    }
}''',
    }
    paths = []
    for name, source in sources.items():
        path = tmp / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(source)
        paths.append(str(path))
    subprocess.run(['javac', '-d', str(tmp), *paths], check=True)
    consumer = analyze(tmp / 'ProtectedDatabaseMaintenance.class')[0]
    traits = {t['id'] for t in consumer['traits']}
    assert not any(t['crit'] >= 4 for t in consumer['traits']), consumer['traits']
    assert 'micro-behaviors/crypto/cipher::jvm-dpapi-jdbc-cipher-references' in traits
    assert 'micro-behaviors/crypto/cipher::jvm-dpapi-base64-gcm-profile' in traits
    assert not any(t.startswith('well-known/lib/platform/jna::') for t in traits)
    identity = analyze(tmp / 'com/sun/jna/platform/win32/Crypt32Util.class')[0]
    assert 'well-known/lib/platform/jna::jna-package-class' in {t['id'] for t in identity['traits']}
    assert 'well-known/lib/platform/jna::platform-win32-package' in {t['id'] for t in identity['traits']}
    for name, source, expected in (
        ('self.php', '<?php unlink(__FILE__);', True),
        ('cache.php', '<?php unlink(__FILE__ . ".cache");', False),
    ):
        path = tmp / name
        path.write_text(source)
        traits = {t['id'] for t in analyze(path)[0]['traits']}
        assert ('micro-behaviors/fs/delete/file/library::self-delete-file-constant' in traits) == expected
print('PASS: JVM maintenance, JNA identity and PHP self-path boundaries')
