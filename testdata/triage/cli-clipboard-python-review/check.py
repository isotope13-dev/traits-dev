"""Static regression controls. Never import or execute the supplied sample."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

args = argparse.ArgumentParser()
args.add_argument('--sample', type=Path, required=True)
args.add_argument('--scratch', type=Path, required=True)
args.add_argument('--baseline-traits', type=Path)
args = args.parse_args()
root = Path(__file__).resolve().parents[3]
source = args.sample.read_text()
prefix = 'objectives/command-and-control/remote-command/http-poll::'
poll = prefix + 'python-async-helper-compiled-exec-poll'
daemon = prefix + 'python-detached-async-helper-exec-poll'
startup = 'objectives/persistence/system/python-startup::startup-hook-async-helper-code-daemon'
neutral = 'micro-behaviors/process/deploy/script-eval::python-http-helper-compiled-exec'
env = 'objectives/exfiltration/stealer/env::python-env-harvest'
enc = 'micro-behaviors/crypto/encrypt::public-key-encrypt-call'
retired = {
    'objectives/supply-chain/credential-theft/env::python-env-harvest',
    'micro-behaviors/crypto/asymmetric/signature::public-key-encrypt-call',
    'objectives/supply-chain/install-hook/build/behavioral/execute::rust-build-rs-command-path',
}


def scan(path):
    text = subprocess.check_output(
        ['cleave', '--traits-dir', str(root), '--format', 'json', str(path)], text=True)
    decoder = json.JSONDecoder()
    files = []
    while text.strip():
        value, end = decoder.raw_decode(text.lstrip())
        text = text.lstrip()[end:]
        files.extend(value['files'])
    return files

with tempfile.TemporaryDirectory(dir=args.scratch) as temp:
    base = Path(temp)
    cases = {}

    def case(name, content, required=(), forbidden=()):
        path = base / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        cases[path] = (set(required), set(forbidden) | retired)

    case('positive/sitecustomize.py', source, {poll, daemon, startup, neutral, env, enc})
    renamed = source
    for old, new in [('fetch_text', 'download_source'), ('exec_code', 'activate_source'),
                     ('cycle', 'refresh'), ('public_key', 'recipient_key'),
                     ('code', 'program'), ('domain', 'server')]:
        import re
        renamed = re.sub(r'\b' + old + r'\b', new, renamed)
    case('renamed.py', renamed, {poll, daemon, neutral, env}, {startup})
    case('httpx.py', source.replace('import requests', 'import httpx as requests')
         .replace('requests.get', 'httpx.get'), {poll, daemon}, {startup})
    case('wrong-mode.py', source.replace("'<remote>', 'exec'", "'<remote>', 'eval'"),
         forbidden={poll, daemon, startup, neutral})
    case('overwritten.py', source.replace('    await exec_code(code)',
         "    code = 'print(1)'\n    await exec_code(code)"),
         forbidden={poll, daemon, startup, neutral})
    case('different-value.py', source.replace('await exec_code(code)', 'await exec_code(text)'),
         forbidden={poll, daemon, startup, neutral})
    case('different-helper.py', source.replace('await exec_code(code)', 'await unrelated(code)'),
         forbidden={poll, daemon, startup, neutral})
    case('different-loop.py', source.replace('asyncio.run(cycle(public_key))',
         'asyncio.run(unrelated(public_key))'), {neutral}, {poll, daemon, startup})
    case('not-http.py', source.replace('asyncio.to_thread(requests.get, url',
         'asyncio.to_thread(read_local, url'), forbidden={poll, daemon, startup, neutral})
    case('single-fetch.py', source.replace('while True:', 'if True:'),
         {neutral}, {poll, daemon, startup})
    case('foreground.py', source.replace('if os.fork():', 'if False:'),
         {poll, neutral}, {daemon, startup})
    case('no-dup.py', source.replace('os.dup2(null, fd)', 'print(fd)'),
         {poll, neutral}, {daemon, startup})
    case('quoted.py', 'example = ' + repr(source) + '\n',
         forbidden={poll, daemon, startup, neutral})
    case('comment.py', '\n'.join('# ' + line for line in source.splitlines()),
         forbidden={poll, daemon, startup, neutral})
    benign = root / 'testdata/benign/litellm-4098-startup/sitecustomize.py'
    case('benign/sitecustomize.py', benign.read_text(), forbidden={poll, daemon, startup, neutral, env})
    # Existing positive fixtures outside this batch exercise retained attack coverage.
    old_env = root / 'testdata/hostile/supply-chain/audit-pypi-direct-env-runtime/source/codec_helper/__init__.py'
    case('env-positive.py', old_env.read_text(), {env})
    case('env-local.py', 'import os\nprint(dict(os.environ))\n', forbidden={env})
    case('encrypt.py', 'public_key.encrypt(message)\n', {enc})
    case('verify.py', 'public_key.verify(signature, message)\n', forbidden={enc})
    case('constructor.rs', 'use std::process::Command;\nfn main() { let command = Command::new(&binary_path); }\n',
         {'micro-behaviors/process/create/direct::rust-indirect-command-new'})
    target_start = 'objectives/supply-chain/install-hook/build/behavioral/execute::rust-build-rs-target-start'
    case('target-start/build.rs',
         'use std::process::Command;\nfn main() { let binary_path = root.join("target"); '
         'Command::new(&binary_path).arg("start").spawn(); }\n', {target_start})
    case('literal.rs', 'fn main() { let label = "binary_path"; }\n',
         forbidden={'micro-behaviors/process/create/direct::rust-indirect-command-new'})
    found = {Path(f['path']): {t['id'] for t in f.get('traits', [])} for f in scan(base)}
    for path, (required, forbidden) in cases.items():
        ids = found.get(path, set())
        assert not (required - ids), (path.name, 'missing', sorted(required - ids))
        assert not (forbidden & ids), (path.name, 'unexpected', sorted(forbidden & ids))
    if args.baseline_traits:
        old = subprocess.check_output(
            ['cleave', '--traits-dir', str(args.baseline_traits), '--format', 'json',
             str(base / 'target-start/build.rs')], text=True)
        assert target_start in old, 'Baseline target-start consumer must also fire'
    # Existing hostile Cargo fixtures must still retain their execution/attack signals.
    for name in ['testdata/drop-exec/build.rs',
                 'testdata/hostile/supply-chain-corpus/rust/crate-glasswingforge-buildrs-embed-drop-linux/build.rs']:
        traits = [t for f in scan(root / name) for t in f.get('traits', [])]
        assert any(t['crit'] >= 4 for t in traits), name
        assert any(t['id'] == 'metadata/build/ecosystem::cargo-build-script-basename' for t in traits), name
    word = 'metadata/lang/natural/vocabulary/content-word::command-word-token'
    for filename, content, expected in [
        ('word.html', '<!doctype html><html><body>Copy the install command</body></html>', True),
        ('flag.vbs', 'shell.Run "powershell -Command Get-Date"', False),
    ]:
        path = base / filename
        path.write_text(content)
        output = subprocess.check_output(
            ['cleave', '--traits-dir', str(root), 'test-rules', str(path), '--rules', word], text=True)
        assert (('\nMATCHED ' + word) in output) == expected, filename
print(f'{len(cases)} controls, 2 word boundaries, and 2 existing hostile Cargo fixtures passed')
