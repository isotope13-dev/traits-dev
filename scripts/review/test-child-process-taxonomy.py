#!/usr/bin/env python3
"""Ensure an unrelated UI marker does not suppress child-process evidence."""
import argparse
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cleave', default='../cleave/target/release/cleave')
args = parser.parse_args()
with tempfile.TemporaryDirectory(prefix='child-process-taxonomy-') as tmp:
    root = Path(tmp)
    launch = 'const {spawn: launch} = require("child_process");\nfunction run() { launch(program).on("exit", callback); }\n'
    cases = {
        'neutral.js': launch,
        'ui.js': launch + 'const x = "__________cytoscape_stylesheet";\n',
        'no-process.js': 'const x = "__________cytoscape_stylesheet";\n',
    }
    for name, source in cases.items():
        (root / name).write_text(source)
    evidence = 'micro-behaviors/process/create/exec::child-process-creation-api'
    for name in cases:
        result = subprocess.run(
            [str((repo / args.cleave).resolve()), '--traits-dir', str(repo), 'test-rules',
             '--rules', evidence, str(root / name)],
            check=True, capture_output=True, text=True,
        )
        expected = 'NOT MATCHED ' if name == 'no-process.js' else 'MATCHED '
        assert expected + evidence in result.stdout, (name, result.stdout)
    print('Child-process evidence survives unrelated UI context.')
