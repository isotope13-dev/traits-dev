#!/usr/bin/env python3
"""Exercise the generic messaging observations after their taxonomy move."""
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', '../cleave/target/release/cleave')
RULES = (
    'micro-behaviors/data/control-flow/event-callback::connection-update-handler-registration',
    'metadata/lang/source/syntax/conditional::connection-open-comparison',
    'micro-behaviors/communications/messaging/send::sendmessage-source-url-reference',
    'micro-behaviors/communications/messaging/send::sendmessage-media-type-reference',
)
CASES = (
    ('match', '''socket.on("connection.update", handler);
if (connection === "open") {
  sendMessage(recipient, {image: {url: "https://example.org/a.png"}, sourceUrl: "https://example.org/a.png"});
}
''', True),
    ('unrelated', '''socket.on("connection.closed", handler);
if (connection === "closed") { console.log("closed"); }
''', False),
)

with tempfile.TemporaryDirectory(prefix='messaging-probe-') as directory:
    for name, source, expected in CASES:
        target = Path(directory) / (name + '.js')
        target.write_text(source + '\n//' + ' padding' * 90 + '\n')
        result = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), 'test-rules',
                                 str(target), '--rules', ','.join(RULES)], cwd=ROOT,
                                capture_output=True, text=True, check=True)
        for rule in RULES:
            prefix = ('MATCHED ' if expected else 'NOT MATCHED ') + rule + ' '
            assert any(line.startswith(prefix) for line in result.stdout.splitlines()), (name, rule, result.stdout)
        print(name + ': passed', flush=True)
