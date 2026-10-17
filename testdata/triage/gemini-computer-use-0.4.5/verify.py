"""Inert source controls for Node signal-call coverage; no fixtures are executed."""
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
SIGNAL = 'micro-behaviors/process/control/signal::node-process-kill-call'


def main():
    dest = Path(sys.argv[1]).resolve()
    dest.mkdir(parents=True, exist_ok=True)
    cases = {
        'forward-self.js': ("process.kill(process.pid, signal);\n", True),
        'probe.js': ("process.kill(pid, 0);\n", True),
        'signal.ts': ("process.kill(pid, 'SIGTERM');\n", True),
        'message.js': ('console.log("process.kill(process.pid, signal)");\n', False),
        'comment.js': ('// process.kill(process.pid, signal)\nconsole.log("done");\n', False),
        'reference.js': ('const send = process.kill;\n', False),
        'different-object.js': ('worker.kill();\n', False),
    }
    for name, (source, _) in cases.items():
        (dest / name).write_text(source)
    result = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
                             '--format', 'json', str(dest)], check=True,
                            stdout=subprocess.PIPE,
                            env={**os.environ, 'CLEAVE_VALIDATE': '0'})
    decoder = json.JSONDecoder()
    remaining = result.stdout.decode().lstrip()
    seen = set()
    while remaining:
        report, end = decoder.raw_decode(remaining)
        remaining = remaining[end:].lstrip()
        for item in report['files']:
            name = Path(item['path']).name
            if name not in cases:
                continue
            traits = item['traits']
            assert (SIGNAL in {t['id'] for t in traits}) == cases[name][1], name
            assert not [t['id'] for t in traits if t['crit'] >= 4], (name, traits)
            seen.add(name)
            print('PASS', name)
    assert seen == set(cases), ('missing cases', set(cases) - seen)


if __name__ == '__main__':
    main()
