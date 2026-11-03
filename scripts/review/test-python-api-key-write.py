#!/usr/bin/env python3
"""Check the interpolated API-key assignment observation."""
import json
import pathlib
import subprocess
import tempfile

cases = {
    'api-key': ('env_file.write_text(f"NVIDIA_API_KEY={api_key}\\n")', True),
    'unrelated-value': ('env_file.write_text(f"PORT={port}\\n")', False),
    'placeholder': ('env_file.write_text("NVIDIA_API_KEY=replace-me\\n")', False),
    'read': ('env_file.read_text()', False),
}
with tempfile.TemporaryDirectory() as tmp:
    for name, (body, expected) in cases.items():
        path = pathlib.Path(tmp) / (name + '.py')
        path.write_text(body + '\n')
        report = json.loads(subprocess.check_output(['../cleave/target/release/cleave', '--traits-dir', '.', '--format', 'json', str(path)]))
        found = any(t['id'].endswith('::pathlib-write-api-key-assignment') for t in report['files'][0].get('traits', []))
        assert found == expected, (name, found, expected)
print('Interpolated API key write boundaries passed.')
