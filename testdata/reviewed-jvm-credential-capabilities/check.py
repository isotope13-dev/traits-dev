#!/usr/bin/env python3
"""Compile inert bytecode controls; no fixture class is executed."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile

p = argparse.ArgumentParser()
p.add_argument('--cleave', default='cleave')
p.add_argument('--scratch', required=True)
a = p.parse_args()
trait_root = Path(__file__).resolve().parents[2]
login = 'objectives/credential-access/browser/chromium::jvm-login-store-copy-and-gcm'
token = 'objectives/credential-access/discord/token::jvm-discord-collector-http-post'
with tempfile.TemporaryDirectory(prefix='jvm-controls-', dir=a.scratch) as directory:
    root = Path(directory)
    sources = {
        'okhttp3/Request.java': 'package okhttp3; public class Request { public static class Builder { public Builder post(Object body) { return this; } } }',
        'okhttp3/MultipartBody.java': 'package okhttp3; public class MultipartBody { public static class Builder {} }',
        'LoginExtraction.java': '''import java.nio.file.*; import java.sql.*;
class LoginExtraction {
 static byte[] gcmDecrypt(byte[] b) { return b; }
 static byte[] read(Path profile, Path target, ResultSet rows) throws Exception {
  Files.copy(profile.resolve("Login Data"), target);
  return gcmDecrypt(rows.getBytes(3));
 }
}''',
        'LoginBackup.java': '''import java.nio.file.*; import java.sql.*;
class LoginBackup {
 static byte[] read(Path profile, Path target, ResultSet rows) throws Exception {
  Files.copy(profile.resolve("Login Data"), target); return rows.getBytes(3);
 }
}''',
        'CipherOnly.java': '''class CipherOnly {
 static byte[] gcmDecrypt(byte[] b) { return b; }
 static byte[] read(byte[] b) { return gcmDecrypt(b); }
}''',
        'TokenSender.java': '''class TokenSender {
 static Object getDiscordTokens() { return null; }
 static void collect() {
  Object values = getDiscordTokens();
  Object builder = new okhttp3.MultipartBody.Builder();
  new okhttp3.Request.Builder().post(values);
 }
}''',
        'TokenOnly.java': '''class TokenOnly {
 static Object getDiscordTokens() { return null; }
 static Object collect() { return getDiscordTokens(); }
}''',
        'PostOnly.java': '''class PostOnly {
 static void send(Object value) {
  Object builder = new okhttp3.MultipartBody.Builder();
  new okhttp3.Request.Builder().post(value);
 }
}''',
    }
    for name, source in sources.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(source)
    subprocess.run(['javac', '-g:none', '-d', str(root)] + [str(root / n) for n in sources], check=True)
    expected = {
        'LoginExtraction.class': {login}, 'LoginBackup.class': set(),
        'CipherOnly.class': set(), 'TokenSender.class': {token},
        'TokenOnly.class': set(), 'PostOnly.class': set(),
    }
    # Same archive, unrelated classes: capability fragments must not pool.
    subprocess.run(['jar', 'cf', str(root / 'separate.jar'), '-C', str(root),
                    'LoginBackup.class', '-C', str(root), 'CipherOnly.class',
                    '-C', str(root), 'TokenOnly.class', '-C', str(root), 'PostOnly.class'], check=True)
    expected['separate.jar'] = set()
    env = dict(os.environ, CLEAVE_TRAITS_DIR=str(trait_root), CLEAVE_SKIP_CACHE='1')
    run = subprocess.run([a.cleave, '--traits-dir', str(trait_root), '--format', 'json'] +
                         [str(root / n) for n in expected], env=env, capture_output=True, text=True, check=True)
    reports = []
    remaining = run.stdout.strip()
    decoder = json.JSONDecoder()
    while remaining:
        entry, end = decoder.raw_decode(remaining)
        reports.append(entry)
        remaining = remaining[end:].lstrip()
    report = {'files': [item for entry in reports for item in entry['files']]}
    for name, want in expected.items():
        matched = set()
        for item in report['files']:
            path = item['path']
            if path == str(root / name) or path.startswith(str(root / name) + '!!'):
                matched.update(t['id'] for t in item.get('traits', []) if t['id'] in {login, token})
        assert matched == want, (name, matched, want)
    print('PASS: two positive bytecode controls and five near misses')
