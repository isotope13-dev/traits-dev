#!/usr/bin/env python3
"""Exercise npm finding accuracy and future resource-exhaustion variants."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile

PHP = 'micro-behaviors/communications/url/http-path/resource::npm-script-php-url-reference'
OLD_PHP = 'command-and-control/endpoint/php'
FORK = 'objectives/impact/dos/fork-bomb::shell-executes-fork-bomb'
DOCKER_FORK = 'objectives/impact/dos/fork-bomb::container-shell-executes-fork-bomb'
RECURSION = 'objectives/impact/dos/fork-bomb::recursive-shell-function-pipeline'
MEMORY = 'objectives/impact/dos/memory::shell-node-unbounded-buffer-retention'
NODE = 'objectives/impact/dos/memory::node-unbounded-buffer-retention'
SPAWN = 'micro-behaviors/process/daemonize/spawn::node-spawn-detached-option'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cleave', default='../cleave/target/release/cleave')
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[2]
    cases = {}

    def case(name, source, required=(), forbidden=(), attack=False):
        cases[name] = (source, set(required), set(forbidden), attack)

    def manifest(name, script, php):
        case(name + '/package.json', json.dumps({'name': 'reference-client', 'version': '1.0.0',
                                                 'scripts': {'check': script}}),
             [PHP] if php else [], [OLD_PHP] + ([] if php else [PHP]))

    manifest('php-local', 'php -f test.php', False)
    manifest('php-config', 'php vendor/bin/php-cs-fixer fix --config=.php-cs-fixer.dist.php', False)
    manifest('php-remote', 'curl https://example.test/api.php', True)
    manifest('php-query', 'curl https://example.test/api.php?format=json', True)
    manifest('php-quoted', 'curl "https://example.test/api.php" --silent', True)
    manifest('php-echo', 'echo https://example.test/api.php', True)  # A reference, not a contact claim.
    manifest('php-query-only', 'curl https://example.test/index.json?redirect=file.php', False)
    manifest('php-host-only', 'curl https://api.php.example.test/index.json', False)
    manifest('php-extension-near-miss', 'curl https://example.test/api.phpdata', False)
    manifest('php-local-scheme', 'cat file:///tmp/api.php', False)

    names = [
        ('uuid.py', 'python-uuid-or-base-module-name'),
        ('shlex.py', 'python-shlex-multicall-subprocess-name'),
        ('os.py', 'python-os-or-sys-module-name'),
        ('test_typing.py', 'python-regression-libpython-typing-name'),
        ('test_subprocess.py', 'python-bytes-os-subprocess-test-name'),
        ('test_future.py', 'python-future-window-asyncgen-name'),
        ('window.py', 'python-future-window-asyncgen-name'),
        ('dbapi.py', 'python-dbapi-fixers-util-name'),
        ('_bootstrap.py', 'python-import-bootstrap-module-name'),
        ('runpy.py', 'python-importlib-runpy-optparse-name'),
        ('shutil.py', 'python-shutil-or-zipimport-name'),
    ]
    for filename, id in names:
        case('names/' + filename, 'value = 1\n', ['metadata/filename/source::' + id])
    case('names/unrelated.py', 'value = 1\n', forbidden=[
        'metadata/filename/source::python-future-window-asyncgen-name'])

    loop = 'const held=[]; while(true) held.push(Buffer.alloc(1024*1024));\n'
    case('memory/while.js', loop, [NODE], attack=True)
    case('memory/while.ts', loop, [NODE], attack=True)
    case('memory/block.js', loop.replace('held.push(Buffer.alloc(1024*1024));', '{ held.push(Buffer.alloc(1024*1024)); }'), [NODE], attack=True)
    case('memory/for.js', loop.replace('while(true)', 'for(;;)'), [NODE], attack=True)
    case('memory/for-block.js', loop.replace('while(true) held.push(Buffer.alloc(1024*1024));', 'for(;;) { held.push(Buffer.allocUnsafe(1024)); }'), [NODE], attack=True)
    case('memory/comments.js', loop.replace('held.push', '/* retain */ held.push'), [NODE], attack=True)
    case('memory/finite.js', loop.replace('while(true)', 'for(let i=0;i<3;i++)'), forbidden=[NODE])
    case('memory/break.js', loop.replace('held.push(Buffer.alloc(1024*1024));', '{ held.push(Buffer.alloc(1024*1024)); break; }'), forbidden=[NODE])
    case('memory/eviction.js', loop.replace('held.push(Buffer.alloc(1024*1024));', '{ held.push(Buffer.alloc(1024*1024)); held.shift(); }'), forbidden=[NODE])
    case('memory/discarded.js', 'while(true) Buffer.alloc(1024);\n', forbidden=[NODE])
    case('memory/zero.js', loop.replace('1024*1024', '0'), forbidden=[NODE])
    case('memory/conditional.js', 'const held=[]; while(true) { if(wantMore) held.push(Buffer.alloc(1024)); }\n', forbidden=[NODE])
    case('memory/comment.js', '// ' + loop, forbidden=[NODE])
    case('memory/string.js', 'const example=' + json.dumps(loop) + ';\n', forbidden=[NODE])
    case('memory/logged.js', 'console.log(' + json.dumps(loop) + ');\n', forbidden=[NODE])
    case('memory/mismatched-array.js', loop.replace('held.push', 'other.push'), forbidden=[NODE])
    case('memory/custom-push.js', 'const held={push(x){}}; while(true) held.push(Buffer.alloc(1024));\n', forbidden=[NODE])
    case('memory/unknown-receiver.js', 'while(true) held.push(Buffer.alloc(1024));\n', forbidden=[NODE])

    bomb = ':(){ :|:& };:'
    docker = f'docker exec "$BOX" bash -c \'{bomb}\'\n'
    case('fork/login.sh', f"bash -lc '{bomb}'\n", [FORK], attack=True)
    case('fork/options.sh', f"sh -ec '{bomb}'\n", [FORK], attack=True)
    case('fork/absolute-docker.sh', '/usr/bin/' + docker, [DOCKER_FORK], attack=True)
    case('fork/timeout-signal.sh', 'timeout --signal=KILL 8s ' + docker, [DOCKER_FORK], attack=True)
    case('fork/absolute-shell.sh', docker.replace('bash -c', '/bin/bash -lc'), [DOCKER_FORK], attack=True)
    case('fork/renamed.sh', 'replicate(){ replicate | replicate & }; replicate\n', [RECURSION], attack=True)
    case('fork/keyword.sh', 'function replicate() { replicate | replicate & }; replicate\n', [RECURSION], attack=True)
    case('fork/different-consumer.sh', 'replicate(){ replicate | cat; }; replicate\n', forbidden=[RECURSION])
    case('fork/stopping-branch.sh', 'replicate(){ if [ "$1" -gt 0 ]; then replicate | replicate & fi; }\n', forbidden=[RECURSION])
    case('fork/comment.sh', '# replicate(){ replicate | replicate & }; replicate\n', forbidden=[RECURSION])
    case('fork/echo.sh', "echo 'replicate(){ replicate | replicate & }; replicate'\n", forbidden=[RECURSION])

    memory = ('docker exec "$BOX" sh -c \'exec 2>/dev/null; '
              'node -e "const held=[];while(true)held.push(Buffer.alloc(50*1024*1024))" \'\n')
    case('shell-memory/login.sh', memory.replace('sh -c', 'bash -lc'), [MEMORY], attack=True)
    case('shell-memory/absolute.sh', '/usr/bin/' + memory, [MEMORY], attack=True)
    case('shell-memory/block.sh', memory.replace('const held=[];while(true)held.push(Buffer.alloc(50*1024*1024))', 'let held = [] ; while ( true ) { held.push(Buffer.alloc(50 * 1024)); }'), [MEMORY], attack=True)
    case('shell-memory/long-flag.sh', memory.replace('node -e', 'node --eval'), [MEMORY], attack=True)
    case('shell-memory/exec-replaces-shell.sh', memory.replace('exec 2>/dev/null;', 'exec echo done;'), forbidden=[MEMORY])
    case('shell-memory/break.sh', memory.replace('while(true)held.push(Buffer.alloc(50*1024*1024))', 'while(true){held.push(Buffer.alloc(50*1024*1024));break;}'), forbidden=[MEMORY])
    case('shell-memory/string-body.sh', memory.replace('const held=[];while(true)held.push(Buffer.alloc(50*1024*1024))', r'const example=\"[];while(true)held.push(Buffer.alloc(50*1024*1024))\"'), forbidden=[MEMORY])
    case('shell-memory/echo.sh', 'echo ' + memory, forbidden=[MEMORY])

    case('spawn/detached.ts', 'spawn(cmd,args,{env: cleanEnv, detached:true, stdio:"pipe"});\n', [SPAWN])
    case('spawn/attached.js', 'spawn(cmd,args,{detached:false});\n', forbidden=[SPAWN])
    case('spawn/comment.js', '// spawn(cmd,args,{detached:true});\n', forbidden=[SPAWN])
    case('spawn/unused-option.js', 'const options={detached:true}; unrelated(cmd,args);\n', forbidden=[SPAWN])
    case('spawn/unrelated-call.js', 'configure(cmd,args,{detached:true});\n', forbidden=[SPAWN])

    with tempfile.TemporaryDirectory(prefix='npm-bad-improve-') as temporary:
        work = Path(temporary) / 'samples'
        work.mkdir()
        for name, (content, *_rest) in cases.items():
            p = work / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content)
        env = {**os.environ, 'XDG_CACHE_HOME': str(Path(temporary) / 'cache')}
        result = subprocess.run([str((repo / args.cleave).resolve()), '--traits-dir', str(repo),
                                 '--format=json', str(work)], capture_output=True, text=True,
                                check=True, env=env)
        reports = [json.loads(line) for line in result.stdout.split('\n') if line.strip()]
        observed = {str(Path(r['files'][0]['path']).relative_to(work)): r['files'] for r in reports}
        assert set(observed) == set(cases), set(observed) ^ set(cases)
        for name, (_content, required, forbidden, attack) in cases.items():
            traits = [t for f in observed[name] for t in f.get('traits', [])]
            ids = {t['id'] for t in traits}
            assert required <= ids, (name, 'missing', required - ids)
            assert not forbidden & ids, (name, 'unexpected', forbidden & ids)
            if name.startswith('names/'):
                assert not [id for id in ids if id.startswith('well-known/lib/stdlib/python-stdlib::p-')], name
                assert 'metadata/build/generated::python-loader-or-stub-context' not in ids, name
            if not attack:
                elevated = [t['id'] for t in traits if t['crit'] >= 4]
                assert not elevated, (name, 'elevated findings', elevated)
            print('PASS', name)
    print(f'{len(cases)} npm bad improvement controls passed')


if __name__ == '__main__':
    main()
