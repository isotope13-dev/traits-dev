#!/usr/bin/env python3
"""Check cross-member RBAC configuration and extension observations."""

import json
import pathlib
import subprocess
import tempfile
import zipfile

CASES = {
    "disabled": ('false', '/hivemq-allow-all-extension', True),
    "enabled": ('true', '/hivemq-allow-all-extension', False),
    "other-extension": ('false', '/hivemq-rbac-extension', False),
}

with tempfile.TemporaryDirectory() as tmp:
    for name, (value, extension, expected) in CASES.items():
        path = pathlib.Path(tmp) / f"{name}.zip"
        with zipfile.ZipFile(path, 'w') as archive:
            archive.writestr('runner.sh', f'#!/bin/sh\ncp -r {extension} /opt/extensions\n')
            archive.writestr('settings.yaml', f'env:\n  - name: RBAC_ENABLED\n    value: "{value}"\n')
        result = subprocess.check_output(
            ["../cleave/target/release/cleave", "--traits-dir", ".", "--format", "json", str(path)]
        )
        root = json.loads(result)["files"][0]
        actual = any(t['id'].endswith('::rbac-false-and-allow-all-extension') for t in root.get('traits', []))
        assert actual == expected, (name, actual, expected)

print("RBAC archive context boundaries passed.")
