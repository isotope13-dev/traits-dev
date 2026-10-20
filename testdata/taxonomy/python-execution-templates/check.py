#!/usr/bin/env python3
"""Scan source without executing it; distinguish templates from active code."""
import argparse
import concurrent.futures
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
GEN = 'micro-behaviors/metaprogramming/generation::python-returned-exec-template'
CHAIN = 'micro-behaviors/process/deploy/script-eval::python-exec-zlib-marshal-chain'
PACK = 'objectives/anti-static/pack/runtime::exec-marshal-zlib'
EXEC = 'micro-behaviors/process/interpreter/eval/direct::exec-builtin'
SEND = 'micro-behaviors/communications/messaging/send::pytelegrambotapi-send-document'


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--scratch', required=True, type=Path)
    ap.add_argument('--cleave', default='cleave')
    args = ap.parse_args()
    with tempfile.TemporaryDirectory(prefix='source-review-', dir=args.scratch) as temp:
        def scan(name):
            path = Path(temp) / name
            shutil.copyfile(HERE / name, path)
            result = subprocess.run(
                [args.cleave, '--traits-dir', str(ROOT), '--format', 'json', str(path)],
                text=True, capture_output=True, check=False,
            )
            assert result.returncode == 0, result.stderr
            report = json.loads(result.stdout)
            traits = {t['id']: t for f in report['files'] for t in f.get('traits', [])}
            if name == 'generator.py':
                assert GEN in traits, traits.keys()
                assert EXEC not in traits, traits.keys()
                assert not any(t['crit'] >= 4 for t in traits.values()), traits.keys()
            elif name == 'decoder-generator.py':
                assert GEN not in traits
                assert 'micro-behaviors/data/decode/base64::b64decode-call' in traits
            elif name == 'active.py':
                assert GEN not in traits, traits.keys()
                assert EXEC in traits and CHAIN in traits and PACK in traits, traits.keys()
                assert traits[PACK]['crit'] == 4, traits[PACK]
            elif name == 'unrelated.py':
                assert EXEC in traits and CHAIN not in traits and PACK not in traits, traits.keys()
            elif name == 'telegram.py':
                assert SEND in traits, traits.keys()
                assert not any(t['crit'] >= 4 for t in traits.values()), traits.keys()
            elif name == 'transforms.py':
                assert 'micro-behaviors/data/decode/base85::b85decode-script' in traits
                assert 'micro-behaviors/data/decode/base85::python-ascii85-decode' in traits
                assert 'micro-behaviors/data/encoding/xor::python-xor-bytes-variable-key' in traits
                assert not any(t.startswith('micro-behaviors/data/encode/base85::') for t in traits)
            elif name == 'uri-eval.js':
                assert 'micro-behaviors/process/interpreter/eval/direct::js-eval-url-decoded' in traits
                assert not any(t['crit'] >= 4 for t in traits.values()), traits.keys()
                assert not any(t.startswith('objectives/supply-chain/') for t in traits)
            return name
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            for name in pool.map(scan, ['generator.py', 'active.py', 'unrelated.py', 'telegram.py', 'transforms.py', 'uri-eval.js', 'decoder-generator.py']):
                print('PASS', name)


if __name__ == '__main__':
    main()
