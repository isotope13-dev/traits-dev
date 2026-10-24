#!/usr/bin/env python3
"""Static regressions against the real samples; never executes their code."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import subprocess

CLIPPER = 'objectives/impact/crypto-manipulation/clipboard::managed-multicoin-clipboard-replacement-template'
LOADER = 'objectives/execution/payload/script-eval::obfuscated-http-xor-inline-stage-loader'
HIDDEN = 'objectives/evasion/process/hidden/window::obfuscated-http-stage-hidden-child'
RENDEZVOUS = 'objectives/command-and-control/channel/deaddrop/blockchain::obfuscated-ethereum-recipient-stage-rendezvous'
HANDLE = 'objectives/credential-access/browser/multi-target::native-browser-file-handle-theft'
KEY = 'objectives/credential-access/browser/multi-target::native-browser-key-material-theft'
TASK = 'objectives/persistence/login/scheduled-task/cli::managed-clipper-hidden-logon-task-template'
ROOT = Path(__file__).resolve().parents[2]


def scan(path):
    result = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
                             '--json', str(path)], capture_output=True, text=True)
    if result.returncode or 'validation failed' in result.stderr:
        raise AssertionError(result.stderr[:6000])
    report = json.loads(result.stdout)
    return {t['id'] for f in report['files'] for t in f.get('traits', [])}


def replace_all_encodings(data, old, new):
    assert len(old) == len(new)
    return data.replace(old, new).replace(old.decode().encode('utf-16le'),
                                       new.decode().encode('utf-16le'))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--native', type=Path, required=True)
    parser.add_argument('--previous-native', type=Path, required=True)
    parser.add_argument('--decoded', type=Path, required=True)
    parser.add_argument('--pretty', type=Path, required=True)
    parser.add_argument('--scratch', type=Path, required=True)
    args = parser.parse_args()
    args.scratch.mkdir(parents=True, exist_ok=True)
    jobs = []

    def add(label, data, suffix, present=(), absent=()):
        path = args.scratch / (label + suffix)
        path.write_bytes(data)
        jobs.append((label, path, set(present), set(absent)))

    native = args.native.read_bytes()
    add('native', native, '.exe', (CLIPPER, HANDLE, KEY, TASK))
    add('no-logon-task', replace_all_encodings(native, b'<LogonTrigger>', b'<OtherTrigger>'), '.exe', (CLIPPER, HANDLE, KEY), (TASK,))
    add('no-hidden-task', replace_all_encodings(native, b'<Hidden>true</Hidden>', b'<Hidden>null</Hidden>'), '.exe', (CLIPPER, HANDLE, KEY), (TASK,))
    add('previous-native', args.previous_native.read_bytes(), '.exe', (CLIPPER, HANDLE, KEY))
    # Real behavior controls remove an effect or its currency/replacement source.
    add('clipper-no-write', native.replace(b'TrySetText(replacement', b'TryGetText(replacement'),
        '.exe', (HANDLE, KEY), (CLIPPER,))
    add('clipper-no-map-result', native.replace(b'replacement = addr', b'candidate__ = addr'),
        '.exe', (HANDLE, KEY), (CLIPPER,))
    add('clipper-legacy-wrapper', native.replace(b'ClipRelayHub', b'ClipboardHub'),
        '.exe', (CLIPPER, HANDLE, KEY))
    for name, path in [('decoded', args.decoded), ('pretty', args.pretty)]:
        data = path.read_bytes()
        add(name, data, '.js', (LOADER, HIDDEN, RENDEZVOUS))
        add(name + '-other-route', data.replace(b':443/0x/cl', b':443/1y/ab')
            .replace(b':443/0x/ls', b':443/1y/cd'), '.js', (LOADER, HIDDEN, RENDEZVOUS))
        add(name + '-visible-child', data.replace(b'windowsHide', b'windowState'),
            '.js', (LOADER, RENDEZVOUS), (HIDDEN,))
        add(name + '-no-eval', data.replace(b'](eval,', b'](noop,'),
            '.js', (), (LOADER, HIDDEN, RENDEZVOUS))
    # A benign background task has the options but no acquired/XOR/eval payload.
    add('benign-detached-helper', b"const {spawn}=require('child_process');"
        b"spawn(process.execPath,['worker.js'],{detached:!0,stdio:'ignore',"
        b"windowsHide:!0}).unref();", '.js', (), (LOADER, HIDDEN, RENDEZVOUS))

    def check(job):
        label, path, present, absent = job
        found = scan(path)
        assert present <= found, (label, 'missing', sorted(present - found))
        assert not absent & found, (label, 'unexpected', sorted(absent & found))
        return label

    with ThreadPoolExecutor(max_workers=3) as pool:
        for label in pool.map(check, jobs):
            print('PASS', label, flush=True)
    print(f'PASS: {len(jobs)} static controls')


if __name__ == '__main__':
    main()
