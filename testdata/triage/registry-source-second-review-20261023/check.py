#!/usr/bin/env python3
"""Offline matcher controls; specimens are never sent to a live service."""
import argparse
import io
import json
import os
from pathlib import Path
import runpy
import subprocess
from unittest.mock import patch

parser = argparse.ArgumentParser()
parser.add_argument('--output', type=Path, required=True)
parser.add_argument('--samples', type=Path, required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parents[3]
args.output.mkdir(parents=True, exist_ok=True)
inputs = args.output / 'inputs'
inputs.mkdir(exist_ok=True)
load = 'micro-behaviors/process/interpreter/eval/source::php-restore-then-include-same-path'
hidden_load = 'objectives/execution/payload/script-eval::wordpress-concealed-restored-file-include'
restorers = {'objectives/persistence/system/supervised::wordpress-concealed-memory-restoration',
             'objectives/persistence/system/supervised::wordpress-concealed-option-restoration'}
os_cmd = 'micro-behaviors/process/create/shell/command-string::erlang-os-cmd-call-syntax'
port = 'metadata/lang/source/syntax/assignment::erlang-port-1050-assignment'
policy = 'micro-behaviors/fs/path/secret-config::sma-policy-config-path'
aead = 'micro-behaviors/crypto/decrypt::rust-aead-decrypt'
padded = 'micro-behaviors/crypto/decrypt::rust-padded-block-decrypt-call'
kdf = 'micro-behaviors/crypto/kdf/algorithm::rust-pbkdf2-hmac-call'
keyring = 'micro-behaviors/os/security/keyring::rust-keyring-get-secret-call'
cases = []

def case(name, text, yes=(), no=(), no_hostile=False):
    path = inputs / name
    path.write_text(text)
    cases.append((path, set(yes), set(no), no_hostile))

php = (args.samples / 'e59c538b12ad/direct-db-mesh.php').read_text()
case('renamed-plugin.php', php, {load, hidden_load} | restorers)
case('other-include.php', php.replace('include $target;', 'include $bootstrap;'), no={load, hidden_load})
case('path-reassigned.php', php.replace('include $target;', '$target = $bootstrap;\n    include $target;'), no={load, hidden_load})
case('branch-reassigned.php', php.replace('chmod($target, 0644);', '$target = $bootstrap;'), no={load, hidden_load})
case('write-argument-side-effect.php', php.replace('file_put_contents($target, $source)', "file_put_contents($target, $target = 'bootstrap.php')"), no={load, hidden_load})
case('unrelated-call.php', php.replace('chmod($target, 0644);', 'mutate($target);'), no={load, hidden_load})
case('visible-plugin.php', php[php.index('add_action'):].join(['<?php\n', '']), {load}, {hidden_load}, True)
case('simple-restore.php', '<?php\nif (!file_exists($file)) { file_put_contents($file, $bytes); }\ninclude $file;\n', {load}, {hidden_load}, True)
case('quoted-restore.php', '<?php\n$example = "if (!file_exists($file)) { file_put_contents($file, $bytes); } include $file;";\n', no={load, hidden_load}, no_hostile=True)
case('erlang-admin.py', '''ERLANG_PORT = 1050
message = 'os:cmd("id")'
''', {os_cmd, port}, no_hostile=True)
case('policy-path-only.py', 'path = "/usr/local/extranet/etc/policy_file.xml"\n', {policy}, no_hostile=True)
case('sma-decrypt.py', 'path = "/usr/local/extranet/etc/policy_file.xml"\nplaintext = cipher.decrypt(data)\n', {'objectives/credential-access/vpn/config::sma-policy-credential-decrypt'})
case('sma-declaration.py', 'path = "/usr/local/extranet/etc/policy_file.xml"\ndef helper_decrypt(data):\n return data\n', {policy}, {'objectives/credential-access/vpn/config::sma-policy-credential-decrypt'}, True)
case('aead.rs', '''use aes_gcm::Aes256Gcm as Cipher;
fn demo() { let renamed = Cipher::new(key); renamed.decrypt(nonce, ciphertext); }
''', {aead}, no_hostile=True)
case('chacha.rs', '''use chacha20poly1305::ChaCha20Poly1305;
fn demo() { let cipher = ChaCha20Poly1305::new(key); cipher.decrypt(nonce, ciphertext); }
''', {aead}, no_hostile=True)
case('other-decrypt.rs', 'fn demo() { let cipher = Other::new(key); cipher.decrypt(nonce, ciphertext); }\n', no={aead}, no_hostile=True)
case('padded-kdf.rs', 'fn demo() { pbkdf2_hmac::<sha1::Sha1>(pass,salt,1,out); cipher.decrypt_padded_mut::<Pkcs7>(data); }\n', {padded, kdf}, no_hostile=True)
case('crypto-comments.rs', '/* pbkdf2_hmac::<sha1::Sha1>(pass,salt,1,out); cipher.decrypt_padded_mut::<Pkcs7>(data); */\n', no={padded, kdf}, no_hostile=True)
case('keyring.rs', '''fn demo() { let renamed = keyring::Entry::new(service,user).context(error)?; renamed.get_secret(); }
''', {keyring}, no_hostile=True)
case('other-secret.rs', '''fn demo() { let entry = Other::new(service,user); entry.get_secret(); }
''', no={keyring}, no_hostile=True)
for name in ['shared-cache-mesh.php', 'sysv-option-mesh.php', 'direct-db-mesh.php']:
    cases.append((root / 'testdata/hostile/php-offdisk-restoration' / name, restorers, set(), False))
for name in ['visible-cache-restore.php', 'option-query.php', 'shared-cache-only.php']:
    cases.append((root / 'testdata/benign/php-offdisk-restoration' / name, set(), {hidden_load}, True))
cases.append((root / 'testdata/triage/appliance-chain/renamed-payload.sh', {'objectives/execution/exploit/sonicwall-sma::sma-wsproxy-loopback-tunnel'}, set(), False))
cases.append((root / 'testdata/triage/appliance-chain/local-admin-tunnel.sh', set(), set(), True))
cases.append((root / 'testdata/benign/sma-wsproxy-legacy-tag-probe.py', set(), set(), True))
env = dict(os.environ, CLEAVE_VALIDATE='0', CLEAVE_TRAITS_DIR=str(root))
run = subprocess.run(['cleave', '--traits-dir', str(root), '--json', *[str(c[0]) for c in cases]], cwd=root, env=env, capture_output=True, text=True, check=True)
(args.output / 'controls.jsonl').write_text(run.stdout)
(args.output / 'controls.log').write_text(run.stderr)
files = {f['path']: f for line in run.stdout.splitlines() for f in json.loads(line)['files']}
results = []
for path, yes, no, no_hostile in cases:
    traits = {t['id']: t['crit'] for t in files[str(path)].get('traits', [])}
    assert yes <= traits.keys(), (path.name, 'missing', yes - traits.keys())
    assert not no & traits.keys(), (path.name, 'unexpected', no & traits.keys())
    assert not no_hostile or 5 not in traits.values(), (path.name, 'hostile', traits)
    results.append({'case': path.name, 'passed': True})
    print('PASS', path.name)
# Replay the specimen against a stub transport: no live socket, target list or
# external command runs. Record the requests it actually constructs.
requests = []
class Response(io.BytesIO):
    def __enter__(self): return self
    def __exit__(self, *args): self.close()
def urlopen(request, **kwargs):
    requests.append({'url': request.full_url, 'method': request.method,
                     'payload': json.loads(request.data), 'timeout': kwargs.get('timeout')})
    return Response(b'controlled-response')
with patch('urllib.request.urlopen', urlopen):
    code = runpy.run_path(str(args.samples / '13201308404e/sma_wsproxy_exploit.py'), run_name='offline_audit')
    assert code['exploit']('https://example.invalid') is None
assert len(requests) == 3 and all(r['method'] == 'POST' for r in requests)
assert requests[0]['payload'] == {'host': '127.0.0.1', 'port': 1050, 'secure': False}
assert requests[1]['payload']['message'] == 'os:cmd("id; uname -a")'
assert requests[2]['payload']['message'] == 'os:cmd("cat /usr/local/extranet/etc/policy_file.xml")'
(args.output / 'request-replay.json').write_text(json.dumps(requests, indent=2) + '\n')
(args.output / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
print(len(results), 'controls passed; 3 offline requests traced')
