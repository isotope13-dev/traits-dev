#!/usr/bin/env python3
"""Unrelated temporary contexts must not suppress agent config writes."""
from pathlib import Path
import os
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', '../cleave/target/release/cleave')
WRITE = 'micro-behaviors/fs/write/file/target::agent-config-path-near-write'
CLUES = 'objectives/evasion/security-bypass/llm/override::agent-config-approval-bypass-clues'
PREFIX = 'const fs = require("fs");\n'
CASES = [
    ('separate-temp', PREFIX + '''const tempConfig = path.join(tempDir, "opencode.json");
env.OPENCODE_CONFIG = tempConfig;
fs.writeFileSync(".claude/settings.json", "{}");
''', True, False),
    ('separate-worktree', PREFIX + '''const s = `sandbox_mode = "workspace-write"\nnetwork_access = false`;
git(["worktree", "add", "/tmp/tree"]);
writeFileSync(tempPath, renderAgentConfig());
fs.writeFileSync(".claude/settings.json", JSON.stringify({auto_approve: true}));
''', True, True),
    ('ordinary-write', PREFIX + 'fs.writeFileSync(".claude/settings.json", "{}");\n', True, False),
]
with tempfile.TemporaryDirectory(prefix='agent-config-regression-') as directory:
    for name, source, expected_write, expected_clues in CASES:
        target = Path(directory) / (name + '.js')
        target.write_text(source + '// padding\n' * 60)
        result = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), 'test-rules', str(target),
                                 '--rules', WRITE + ',' + CLUES], cwd=ROOT, capture_output=True,
                                text=True, check=True)
        for rule, expected in ((WRITE, expected_write), (CLUES, expected_clues)):
            prefix = ('MATCHED ' if expected else 'NOT MATCHED ') + rule + ' '
            assert any(line.startswith(prefix) for line in result.stdout.splitlines()), (name, rule, result.stdout)
        print(name + ': passed', flush=True)
