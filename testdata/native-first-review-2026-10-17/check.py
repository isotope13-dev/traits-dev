"""Check required call targets, argument relationships, and string near misses."""
import concurrent.futures
import json
import os
import subprocess
import tempfile
from pathlib import Path
from build_controls import image

ROOT = Path(__file__).resolve().parents[2]
ENGINE = os.environ.get('CLEAVE', 'cleave')
GHOST = 'objectives/evasion/process/injection/hollowing/process::delete-pending-image-context-redirection'
DISPOSE = 'objectives/evasion/process/injection/hollowing/process::delete-pending-executable-section'
CONTEXT = 'micro-behaviors/process/inject/runtime/thread-context::x64-context-rcx-write-call'
SHELL = 'micro-behaviors/process/create/shellexec::shell-execute-call'
EDGE = 'metadata/file/string/application-name::edge-name-ms'
CASES = {
    'positive': ({GHOST: 5, DISPOSE: 4, CONTEXT: 4, SHELL: 3, EDGE: 3}, []),
    'wrong-disposition-buffer': ({CONTEXT: 4}, [DISPOSE, GHOST]),
    'wrong-disposition-call': ({CONTEXT: 4}, [DISPOSE, GHOST]),
    'keep-file': ({CONTEXT: 4}, [DISPOSE, GHOST]),
    'non-image-section': ({CONTEXT: 4}, [DISPOSE, GHOST]),
    'wrong-image-call': ({CONTEXT: 4}, [DISPOSE, GHOST]),
    'wrong-context-register': ({DISPOSE: 4}, [CONTEXT, GHOST]),
    'wrong-context-call': ({DISPOSE: 4}, [CONTEXT, GHOST]),
    'autorun-directive': ({DISPOSE: 4, CONTEXT: 4, GHOST: 5}, [SHELL, EDGE]),
}


def check(item):
    index, (name, (expected, absent)) = item
    # Neutral filenames outside the fixture tree prevent name-based exclusions.
    with tempfile.TemporaryDirectory(prefix='native-control-') as tmp:
        target = Path(tmp) / ('control%d.exe' % index)
        target.write_bytes(image(name))
        result = subprocess.run([ENGINE, '--traits-dir', str(ROOT), '--format', 'json', str(target)],
                                capture_output=True, text=True, check=True)
        report = json.loads(result.stdout)
        traits = {t['id']: t['crit'] for f in report['files'] for t in f.get('traits', [])}
        for tid, severity in expected.items():
            assert traits.get(tid) == severity, (name, tid, traits.get(tid), result.stderr)
        for tid in absent:
            assert tid not in traits, (name, tid)
        return 'PASS ' + name


if __name__ == '__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        for result in pool.map(check, enumerate(CASES.items())):
            print(result, flush=True)
    print('%d controls passed' % len(CASES))
