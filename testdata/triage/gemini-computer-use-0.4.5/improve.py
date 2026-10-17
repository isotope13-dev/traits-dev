"""Scan inert controls for CLI resolution, launch arguments, and signal targets.

Usage: python3 testdata/triage/gemini-computer-use-0.4.5/improve.py /tmp/cli-controls
An optional second argument scans the submitted alias archive too.
"""
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
RESOLVE = 'micro-behaviors/os/module/require::node-require-resolve-call'
LAUNCH = 'micro-behaviors/process/create/exec::node-spawn-current-executable'
COMPUTED = 'micro-behaviors/process/create/exec::spawn-variable-program'
SIGNAL = 'micro-behaviors/process/control/signal::node-process-kill-call'
SELF = 'micro-behaviors/process/control/signal::node-process-self-signal-call'
PROBE = 'micro-behaviors/process/control/signal::node-process-liveness-probe'
TARGETS = {RESOLVE, LAUNCH, COMPUTED, SIGNAL, SELF, PROBE}


def reports(data):
    decoder = json.JSONDecoder()
    remaining = data.decode().lstrip()
    while remaining:
        report, end = decoder.raw_decode(remaining)
        yield from report['files']
        remaining = remaining[end:].lstrip()


def main():
    dest = Path(sys.argv[1]).resolve()
    dest.mkdir(parents=True, exist_ok=True)
    cases = {
        'resolve.js': ("require.resolve('worker');", {RESOLVE}),
        'resolve-computed.js': ("require['resolve']('worker');", {RESOLVE}),
        'resolve-spaced.ts': ("require . resolve ('worker');", {RESOLVE}),
        'resolve-reference.js': ("const resolvePath = require.resolve;", set()),
        'resolve-examples.js': ('console.log("require.resolve(\'worker\')");', set()),
        'resolve-comment.js': ("// require.resolve('worker')\nconst x = 1;", set()),
        'runtime-spawn.js': ("spawn(process.execPath, ['worker.js']);", {LAUNCH}),
        'runtime-sync.ts': ("cp.spawnSync(process.execPath, ['worker.js']);", {LAUNCH}),
        'runtime-execfile.js': ("cp.execFile(process.execPath, ['worker.js']);", {LAUNCH}),
        'runtime-execfile-sync.js': ("execFileSync(process.execPath, ['worker.js']);", {LAUNCH}),
        'runtime-computed.js': ("cp['spawn'](process['execPath'], ['worker.js']);", {LAUNCH}),
        'runtime-commented.js': ("spawn(/* executable */ process.execPath, []);", {LAUNCH}),
        'runtime-fork.js': ("fork(process.execPath, ['worker.js']);", set()),
        'runtime-second-arg.js': ("spawn('worker', [process.execPath]);", set()),
        'runtime-second-direct.js': ("spawn('worker', process.execPath);", set()),
        'runtime-other-object.js': ("spawn(config.execPath, []);", set()),
        'runtime-examples.js': ('console.log("spawn(process.execPath, [])");', set()),
        'runtime-comment.js': ("// spawn(process.execPath, [])\nconst x = 1;", set()),
        'computed-program.js': ("cp.spawn(selectProgram(), []);", {COMPUTED}),
        'computed-index.js': ("cp['spawn'](programs[index], []);", {COMPUTED}),
        'ui-instance-spawn.js': ("this.spawn(position);", set()),
        'ui-local-spawn.js': ("spawn( localPosition);", set()),
        'ui-cx-spawn.js': ("spawn(cxPosition);", set()),
        'self-signal.js': ("process.kill(process.pid, signal);", {SIGNAL, SELF}),
        'self-computed.js': ("process['kill'](process['pid'], signal);", {SIGNAL, SELF}),
        'self-commented.js': ("process.kill(/* target */ process.pid, signal);", {SIGNAL, SELF}),
        'self-probe.ts': ("process.kill(process.pid, 0);", {SIGNAL, SELF, PROBE}),
        'other-probe.js': ("process.kill(otherPid, 0x0);", {SIGNAL, PROBE}),
        'zero-in-wrong-argument.js': ("process.kill(0, signal);", {SIGNAL}),
        'self-in-wrong-argument.js': ("process.kill(otherPid, process.pid);", {SIGNAL}),
        'unrelated-pid.js': ("process.kill(otherPid, signal); console.log(process.pid);", {SIGNAL}),
        'signal-reference.js': ("const sendSignal = process.kill;", set()),
        'signal-comment.js': ("// process.kill(process.pid, 0)\nconst x = 1;", set()),
        'signal-examples.js': ('console.log("process.kill(process.pid, 0)");', set()),
    }
    for name in ['runtime-spawn.js', 'runtime-sync.ts', 'runtime-computed.js',
                 'runtime-commented.js', 'runtime-other-object.js']:
        cases[name][1].add(COMPUTED)
    for name, (source, _) in cases.items():
        (dest / name).write_text(source + '\n')
    args = [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
            '--format', 'json', str(dest)]
    if len(sys.argv) > 2:
        args.append(sys.argv[2])
    existing = {
        str(ROOT / 'testdata/benign' / name)
        for name in ['self-daemon-cli-controls.js', 'node-update-check-worker.js',
                     'pinned-release-current-exec-positive.js']
    }
    args.extend(sorted(existing))
    result = subprocess.run(args, check=True, stdout=subprocess.PIPE,
                            env={**os.environ, 'CLEAVE_VALIDATE': '0'})
    seen = set()
    archive_seen = False
    existing_seen = set()
    for item in reports(result.stdout):
        name = Path(item['path']).name
        traits = item['traits']
        ids = {t['id'] for t in traits}
        if name in cases:
            expected = cases[name][1]
            assert ids & TARGETS == expected, (name, sorted(ids & TARGETS), sorted(expected))
            assert not [t['id'] for t in traits if t['crit'] >= 4], name
            seen.add(name)
            print('PASS', name)
        elif len(sys.argv) > 2 and item['path'] == sys.argv[2]:
            assert ids & TARGETS == {RESOLVE, LAUNCH, COMPUTED, SIGNAL, SELF}, sorted(ids & TARGETS)
            assert not [t['id'] for t in traits if t['crit'] >= 4], 'alias archive'
            archive_seen = True
            print('PASS alias archive')
        elif item['path'] in existing:
            assert LAUNCH in ids, (name, 'missing runtime-launch finding')
            assert not [t['id'] for t in traits if t['crit'] >= 4], name
            existing_seen.add(item['path'])
            print('PASS existing benign fixture', name)
    assert seen == set(cases), ('missing controls', set(cases) - seen)
    assert len(sys.argv) <= 2 or archive_seen, 'archive absent from output'
    assert existing_seen == existing, ('missing existing fixtures', existing - existing_seen)


if __name__ == '__main__':
    main()
