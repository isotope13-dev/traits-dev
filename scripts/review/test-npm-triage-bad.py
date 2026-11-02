#!/usr/bin/env python3
"""Check npm regression edge cases without running any sample code."""
import argparse
import base64
import io
import json
import os
from pathlib import Path
import subprocess
import tarfile
import tempfile

FORK = 'objectives/impact/dos/fork-bomb::shell-executes-fork-bomb'
DOCKER_FORK = 'objectives/impact/dos/fork-bomb::container-shell-executes-fork-bomb'
MEMORY = 'objectives/impact/dos/memory::shell-node-unbounded-buffer-retention'
XOR = 'objectives/anti-static/obfuscation/payload/python-embedded::python-xor-blob-import-exec-seal'
ACCEPT = 'micro-behaviors/communications/http/header/accept::python-json-accept-header-text'


def pack(path, files):
    with tarfile.open(path, 'w:gz') as archive:
        for name, source in files.items():
            data = source.encode()
            entry = tarfile.TarInfo(name)
            entry.size = len(data)
            archive.addfile(entry, io.BytesIO(data))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cleave', default='../cleave/target/release/cleave')
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[2]
    bomb = ':(){ :|:& };:'
    dock = f'docker exec "$BOX" bash -c \'{bomb}\'\n'
    memory = ('docker exec "$BOX" sh -c \'exec 2>/dev/null; '
              'node -e "const a=[];while(true)a.push(Buffer.alloc(50*1024*1024))" \'\n')
    decoder = ('import base64\nblob = base64.b64decode("cHJpbnQoJ29rJyk=")\n'
               'key = b"k"\n'
               'source = bytes(value ^ key[index % len(key)] for index, value in enumerate(blob))\n')
    cases = {}

    def case(name, source, required=(), forbidden=(), elevated=False):
        cases[name] = (source, set(required), set(forbidden), elevated)

    case('direct-fork.sh', f"bash -c '{bomb}'\n", [FORK], elevated=True)
    case('absolute-shell.sh', f"/bin/sh -c '{bomb}'\n", [FORK], elevated=True)
    case('spacing-fork.sh', 'bash -c ": () { : | : & }; :"\n', [FORK], elevated=True)
    case('docker-fork.sh', dock, [DOCKER_FORK], elevated=True)
    case('timeout-fork.sh', 'timeout 8 ' + dock, [DOCKER_FORK], elevated=True)
    case('renamed-container.sh', dock.replace('$BOX', 'arbitrary-container'), [DOCKER_FORK], elevated=True)
    case('comment-fork.sh', '# ' + dock, forbidden=[FORK, DOCKER_FORK])
    case('echo-fork.sh', f"echo '{bomb}'\n", forbidden=[FORK, DOCKER_FORK])
    case('assigned-fork.sh', f"example='{bomb}'\n", forbidden=[FORK, DOCKER_FORK])
    case('docker-echo-fork.sh', dock.replace('bash -c', 'echo'), forbidden=[FORK, DOCKER_FORK])
    case('timeout-echo-fork.sh', 'timeout 8 echo ' + dock, forbidden=[FORK, DOCKER_FORK])
    case('docker-copy-fork.sh', dock.replace('docker exec', 'docker cp'), forbidden=[DOCKER_FORK])
    case('docker-memory.sh', memory, [MEMORY], elevated=True)
    case('timeout-memory.sh', 'timeout 8 ' + memory, [MEMORY], elevated=True)
    case('unsafe-allocation.sh', memory.replace('Buffer.alloc(', 'Buffer.allocUnsafe('), [MEMORY], elevated=True)
    case('let-retention.sh', memory.replace('const a', 'let stash').replace('a.push', 'stash.push'), [MEMORY], elevated=True)
    case('finite-loop.sh', memory.replace('while(true)', 'for(let i=0;i<3;i++)'), forbidden=[MEMORY])
    case('released-buffer.sh', memory.replace('a.push(Buffer.alloc(50*1024*1024))', 'Buffer.alloc(50*1024*1024)'), forbidden=[MEMORY])
    case('echo-memory.sh', 'echo ' + memory, forbidden=[MEMORY])
    case('comment-memory.sh', '# ' + memory, forbidden=[MEMORY])
    case('docker-echo-memory.sh', memory.replace('sh -c', 'echo'), forbidden=[MEMORY])
    case('quoted-loop-text.sh', memory.replace('const a=[];', 'console.log('), forbidden=[MEMORY])
    case('xor-loader.py', decoder + 'exec(source)\n', [XOR], elevated=True)
    case('aliased-loader.py', decoder.replace('import base64', 'import base64 as codec').replace('base64.b64decode', 'codec.b64decode') + 'exec(source)\n', [XOR], elevated=True)
    case('guarded-loader.py', decoder + 'if __import__("os").name == "nt":\n    exec(source)\n', [XOR], elevated=True)
    case('unrelated-main.py', decoder + 'print("ordinary initializer")\n', forbidden=[XOR])
    case('deferred-exec.py', decoder + 'def execute_later():\n    exec(source)\n', forbidden=[XOR])
    case('unrelated-base64.py', decoder + 'exec("print(1)")\n', forbidden=[XOR])
    case('quoted-loader.py', 'example = ' + repr(decoder + 'exec(source)\n') + '\n', forbidden=[XOR])
    case('evaluated-string-loader.py', 'example = ' + repr(decoder + 'exec(source)\n') + '\nexec(example)\n', [XOR], elevated=True)
    encoded = base64.b64encode((decoder + 'exec(source)\n').encode()).decode()
    case('encoded-loader.py', 'payload = ' + repr(encoded) + '\n', [XOR], elevated=True)
    case('no-xor-loader.py', decoder.split('key =')[0] + 'exec(blob)\n', forbidden=[XOR], elevated=True)
    case('php-crypto-test.php', '<?php\n$data = "' + 'aB3/+09=' * 600 + '";\nassert(strlen($data)>0);\n', forbidden=['objectives/anti-static/obfuscation/eval/loader::php-encoded-content-dynamic-apis'])
    case('crypto-constants.js', 'const a=Buffer.from("' + 'ab' * 24 + '","hex");\nconst b=Buffer.from("' + 'cd' * 24 + '","hex");\n', ['metadata/lang/source/literal/hex::repeated-node-hex-buffer-constant-text'])
    case('api-key.js', 'const key=process.env.API_KEY;\n', ['micro-behaviors/os/env/read/named::api-key-process-env'])
    case('cpp-keepalive.java', 'class Keepalive { String ping="PING"; String pong="PONG"; }\n', ['metadata/lang/source/literal/string/command::java-ping-literal', 'metadata/lang/source/literal/string/command::java-pong-literal'])
    case('active-status.cs', 'class Status { string status="Active"; string user="User"; string pong="Pong"; }\n', ['metadata/lang/source/literal/string/label::csharp-active-string-literal', 'metadata/lang/source/literal/string/label::csharp-user-string-literal'])
    case('system-info.php', '<?php $method="system_info";\n', ['metadata/lang/source/literal/string/label::php-system-info-string-literal'])
    case('accept-json.py', 'headers={"Accept":"application/json"}\n', [ACCEPT])
    case('aead.cs', 'class Parameters { AeadParameters p; GcmBlockCipher c; }\n', ['micro-behaviors/crypto/symmetric/aead::csharp-aead-parameters-reference', 'micro-behaviors/crypto/cipher::csharp-gcm-block-cipher-reference'])
    post = 'micro-behaviors/communications/http/post::jvm-post-method-source'
    named_post = 'micro-behaviors/data/control-flow/dispatch/named::post-named-call'
    case('view-post.java', 'class UI { void draw() { tableView.post(task); } }\n', [named_post], [post])
    case('http-post.java', 'class Client { void send() { connection.setRequestMethod("POST"); } }\n', [post])
    case('http-post.kt', 'fun send() { connection.requestMethod = "POST" }\n', [post])
    case('post-method.pl', '$client->post($url);\n', [named_post])
    with tempfile.TemporaryDirectory(prefix='npm-bad-controls-') as temporary:
        work = Path(temporary) / 'samples'
        work.mkdir()
        for name, (source, *_rest) in cases.items():
            (work / name).write_text(source)
        archive_cases = {
            'cross-file.tgz': ({'package/package.json': '{"name":"ordinary-sdk","version":"1.0.0"}',
                                'package/decoder.py': decoder, 'package/main.py': 'print("ready")\n',
                                'package/hash.js': 'for(let i=0;i<32;i++){output[i]^=key[i%8];}\n'}, set()),
            'same-file-loader.tgz': ({'package/package.json': '{"name":"renamed","version":"1.0.0"}',
                                      'package/runtime.py': decoder + 'exec(source)\n'}, {XOR}),
        }
        for name, (sources, required) in archive_cases.items():
            pack(work / name, sources)
            cases[name] = ('', required, set() if required else {XOR}, bool(required))
        env = {**os.environ, 'XDG_CACHE_HOME': str(Path(temporary) / 'cache')}
        result = subprocess.run([str((repo / args.cleave).resolve()), '--traits-dir', str(repo),
                                 '--format=json', str(work)], check=True, capture_output=True,
                                text=True, env=env)
        reports = [json.loads(line) for line in result.stdout.split('\n') if line.strip()]
        observed = {Path(r['files'][0]['path']).name: r['files'] for r in reports}
        assert set(observed) == set(cases), ('case mismatch', set(cases) ^ set(observed))
        for name, (_source, required, forbidden, elevated) in cases.items():
            traits = [t for f in observed[name] for t in f.get('traits', [])]
            ids = {t['id'] for t in traits}
            assert required <= ids, (name, 'missing', required - ids)
            assert not forbidden & ids, (name, 'unexpected', forbidden & ids)
            if not elevated:
                assert not [t['id'] for t in traits if t['crit'] >= 4], (name, 'unexpected elevated traits')
            print('PASS', name)
    print(f'{len(cases)} npm bad-triage controls passed')


if __name__ == '__main__':
    main()
