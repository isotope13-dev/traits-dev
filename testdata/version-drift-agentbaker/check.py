"""Check the shell-name near miss and preserve real process/API coverage."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

fixtures = Path(__file__).resolve().parent
root = fixtures.parent.parent
console = 'objectives/command-and-control/infrastructure/operator::cli-operator-console'
retired = 'objectives/command-and-control/infrastructure/operator::foreground-interactive-shell'
command = 'micro-behaviors/process/create/exec::go-exec-command-call'
cases = {
    'shell-name.go': (set(), {console, retired, command}),
    'session-console.go': ({console}, {retired, command}),
    'process-command.go': ({command}, {console, retired}),
}
with tempfile.TemporaryDirectory(prefix='agentbaker-controls-') as directory:
    for name, (required, forbidden) in cases.items():
        target = Path(directory) / name
        shutil.copyfile(fixtures / name, target)
        result = subprocess.run(
            [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(root),
             '--format', 'jsonl', str(target)],
            env={**os.environ, 'CLEAVE_VALIDATE': '0'},
            check=True, capture_output=True, text=True,
        )
        ids = {trait['id'] for line in result.stdout.splitlines()
               for file in json.loads(line).get('files', [])
               for trait in file.get('traits', [])}
        assert required <= ids, (name, 'missing', required - ids)
        assert not forbidden & ids, (name, 'unexpected', forbidden & ids)
        print(name, 'passed')
