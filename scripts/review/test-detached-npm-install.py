#!/usr/bin/env python3
"""Check that the npm install itself, not another child, is detached."""
import io
import json
from pathlib import Path
import subprocess
import tarfile
import tempfile

repo = Path(__file__).resolve().parents[2]
trait = 'micro-behaviors/os/package-manager/runtime-install::npm-package-detached-npm-install'
sources = {
    'detached': "const {spawn}=require('child_process');\n"
                "const c=spawn('npm',['install','demo'],{detached:true,stdio:'ignore'});c.unref();\n",
    'separate': "const {spawn}=require('child_process');\n"
                "const c=spawn('node',['daemon.js'],{detached:true,stdio:'ignore'});c.unref();\n"
                "spawn('npm',['install','demo'],{stdio:'pipe'});\n",
}
with tempfile.TemporaryDirectory(prefix='detached-npm-') as tmp:
    paths = []
    for name, source in sources.items():
        path = Path(tmp) / (name + '.tgz')
        with tarfile.open(path, 'w:gz') as archive:
            for member, data in [
                ('package/package.json', json.dumps({'name': 'fixture', 'version': '1.0.0', 'main': 'cli.js'})),
                ('package/cli.js', source),
            ]:
                raw = data.encode()
                info = tarfile.TarInfo(member)
                info.size = len(raw)
                archive.addfile(info, io.BytesIO(raw))
        paths.append(str(path))
    output = subprocess.run(
        [str((repo / '../cleave/target/release/cleave').resolve()), '--traits-dir', str(repo), '--format=json', *paths],
        check=True, capture_output=True, text=True,
    )
    found = {}
    for line in output.stdout.splitlines():
        root = json.loads(line)['files'][0]
        found[Path(root['path']).stem] = trait in {t['id'] for t in root.get('traits', [])}
    assert found == {'detached': True, 'separate': False}, found
print('Detached npm install is bound to the same call.')
