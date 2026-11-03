#!/usr/bin/env python3
"""Distinguish prompt-content event construction from isolated text."""
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
trait = 'micro-behaviors/os/telemetry/logging/llm::go-prompt-text-event-field'
cases = {
    'prompt.go': ('func f() { fields["prompt"] = map[string]interface{}{"text": prompt}; emitHookEvent(logger, "prompt.submitted", fields) }', True),
    'variant.go': ('func f() { data["prompt"] = map[string]any{"text": msg}; recordEvent("prompt.submitted", data) }', True),
    'no-event.go': ('func f() { fields["prompt"] = map[string]any{"text": prompt} }', False),
    'other-event.go': ('func f() { fields["prompt"] = map[string]any{"text": prompt}; emitEvent("session.start", fields) }', False),
    'comment.go': ('func f() { /* fields["prompt"] = map[string]any{"text": prompt} */ emitEvent("prompt.submitted", fields) }', False),
}
with tempfile.TemporaryDirectory(prefix='go-prompt-event-') as tmp:
    paths = []
    for name, (source, _) in cases.items():
        path = Path(tmp) / name
        path.write_text('package main\n' + source + '\n')
        paths.append(str(path))
    result = subprocess.run(
        [str((repo / '../cleave/target/release/cleave').resolve()), '--traits-dir', str(repo), '--format=json', *paths],
        check=True, capture_output=True, text=True,
    )
    seen = set()
    for line in result.stdout.splitlines():
        f = json.loads(line)['files'][0]
        name = Path(f['path']).name
        actual = trait in {t['id'] for t in f.get('traits', [])}
        assert actual == cases[name][1], (name, actual, cases[name][1])
        seen.add(name)
    assert seen == set(cases), seen
print('Go prompt event boundaries passed.')
