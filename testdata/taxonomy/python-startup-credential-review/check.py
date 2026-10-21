"""Static controls: scan fixture source, never import or execute it."""
import json
from pathlib import Path
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]

def report(path):
    raw = subprocess.check_output(['cleave', '--traits-dir', str(ROOT), '--format', 'json', str(path)], text=True)
    data = json.loads(raw)
    def walk(x):
        if isinstance(x, dict):
            for k, v in x.items():
                if k == 'id' and isinstance(v, str):
                    yield v
                yield from walk(v)
        elif isinstance(x, list):
            for v in x:
                yield from walk(v)
    return set(walk(data))

poll = 'objectives/command-and-control/remote-command/http-poll::python-polled-direct-code-daemon'
proc = 'micro-behaviors/fs/proc/info/path::python-proc-environ-glob'
assert poll in report(HERE / 'poll.py')
assert poll not in report(HERE / 'mismatched.py')
assert proc in report(HERE / 'proc.py')
assert proc not in report(HERE / 'other-root.py')
# These benign controls exercise relocated observations without live effects.
with tempfile.TemporaryDirectory(dir=HERE) as directory:
    base = Path(directory)
    cases = [
        ('sitecustomize.py', 'import os\n',
         'micro-behaviors/process/interpreter/python::sitecustomize-startup-hook', True),
        ('ordinary.py', 'import os\n',
         'micro-behaviors/process/interpreter/python::sitecustomize-startup-hook', False),
        ('history.py', "from pathlib import Path\ndata = Path('.bash_history').read_text()\n",
         'micro-behaviors/fs/read/file/target::shell-history-path-near-file-read', True),
        ('data.py', "from pathlib import Path\ndata = Path('data.txt').read_text()\n",
         'micro-behaviors/fs/read/file/target::shell-history-path-near-file-read', False),
        ('registry.py', "from pathlib import Path\npaths = ['.docker/config.json', '.npmrc']\nfor p in paths:\n    data = Path(p).read_text()\n",
         'micro-behaviors/fs/read/file/target::registry-credential-path-read-cluster', True),
        ('docker.py', "from pathlib import Path\ndata = Path('.docker/config.json').read_text()\n",
         'micro-behaviors/fs/read/file/target::registry-credential-path-read-cluster', False),
        ('METADATA', 'Metadata-Version: 2.1\nName: litellm\nVersion: 1.0\n',
         'metadata/package/name/identity::litellm-pkginfo-name', True),
        ('PKG-INFO', 'Metadata-Version: 2.1\nName: unrelated\nVersion: 1.0\n',
         'metadata/package/name/identity::litellm-pkginfo-name', False),
        ('copilot.py', "path = '.config/github-copilot/hosts.json'\n",
         'micro-behaviors/fs/path/credential::copilot-hosts-auth-artifact-path', True),
        ('hosts.py', "path = '.config/unrelated/hosts.json'\n",
         'micro-behaviors/fs/path/credential::copilot-hosts-auth-artifact-path', False),
    ]
    for filename, source, trait, expected in cases:
        path = base / filename
        path.write_text(source)
        assert (trait in report(path)) == expected, (filename, trait)
print('14 static positive and near-miss controls passed')
