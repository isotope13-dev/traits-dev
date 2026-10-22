"""Static PE controls for call-only credential rules and input reporting.
Usage: python3 testdata/go-stealer-native-input-review/verify.py <scratch-dir>
Generated files are inert and never executed. Real positive samples and the
upstream kernel-allocation control are recorded in analysis.json.
"""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location(
    'pe_controls', ROOT / 'testdata/native-rat-loader-triage/verify.py')
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)

KEY = 'objectives/collection/keylog/hook::native-hook-key-event-reporting'
STACK = ('objectives/anti-static/obfuscation/control-flow/stack::'
         'x64-repeated-stack-copy-jump-dispatch')
POOL = 'micro-behaviors/mem/alloc/executable::nonpaged-pool'
USAGE = 'micro-behaviors/mem/query::nonpaged-pool-usage-field-reference'
NX = 'micro-behaviors/mem/alloc/heap::nonpaged-pool-nx-session-flag-reference'
EDGE = 'micro-behaviors/os/com/invoke::edge-ielevator-interface-guid-readonly'
NEW_CREDENTIAL = (
    'go-raw-browser-credentials-with-master-key',
    'go-stored-discord-token-decryption',
    'go-wallet-directory-credential-sweep',
    'go-reflective-browser-key-extractor',
    'go-browser-wallet-archive-encrypted-sender',
)


def main():
    dest = Path(sys.argv[1])
    dest.mkdir(parents=True, exist_ok=True)
    hook = b'NtUserSetWindowsHookEx\0'
    report = b' flags=0x\0 time=\0 scan=0x\0 vk=\0SYSKEYUP\0'
    dispatch = bytes.fromhex(
        'FF 34 24 FF 34 24 58 48 81 C4 08 00 00 00 '
        '48 81 C4 08 00 00 00 E9 00 00 00 00')
    markers = (b'app_bound_encrypted_key\0Login Data\0'
               b'sym.go.example.ExtractMasterKeyV10\0'
               b'sym.go.example.ReadLockedFileEx\0'
               b'sym.go.example.EncryptAndSend\0'
               b'sym.go.example.copyWalletDir\0')
    cases = [
        ('input-report.exe', hook + report, '.rdata', {KEY}, {STACK}),
        ('hook-only.exe', hook, '.rdata', set(), {KEY, STACK}),
        ('report-only.exe', report, '.rdata', set(), {KEY, STACK}),
        ('pool-usage.exe', b'quotaNonPagedPoolUsage\0', '.rdata', {USAGE}, {POOL}),
        ('pool-flag.exe', b'NonPagedPool\0', '.rdata', {POOL}, {USAGE}),
        ('pool-nx.exe', b'NonPagedPoolNx\0', '.rdata', {NX}, {POOL, USAGE}),
        ('pool-execute.exe', b'NonPagedPoolExecute\0', '.rdata', {POOL}, {NX, USAGE}),
        ('edge-interface.exe', bytes.fromhex('07 B8 C2 C9 31 77 34 4F 81 B7 44 FF 77 79 52 2B'), '.rdata', {EDGE}, {KEY, STACK}),
        ('names-without-calls.exe', markers, '.rdata', set(), {KEY, STACK}),
        ('stack-dispatch.exe', dispatch * 8, '.themida', {STACK}, {KEY}),
        ('stack-seven.exe', dispatch * 7, '.themida', set(), {KEY, STACK}),
        ('stack-in-data.exe', dispatch * 8, '.rdata', set(), {KEY, STACK}),
    ]
    results = []
    for name, data, section, present, absent in cases:
        if len(sys.argv) > 2 and name not in sys.argv[2:]:
            continue
        path = dest / name
        path.write_bytes(helper.pe_image(data=data, data_section=section))
        run = subprocess.run(
            [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
             '--format', 'json', str(path)],
            env=dict(os.environ, CLEAVE_VALIDATE='0'), check=True,
            text=True, capture_output=True)
        report = json.loads(run.stdout)
        ids = {t['id'] for f in report['files'] for t in f['traits']}
        assert present <= ids, (name, 'missing', present - ids)
        assert not absent & ids, (name, 'unexpected', absent & ids)
        assert not any(x.split('::')[-1] in NEW_CREDENTIAL for x in ids), (name, ids)
        results.append({'name': name, 'present': sorted(present), 'absent': sorted(absent)})
        print('PASS', name, flush=True)
    (dest / 'results.json').write_text(json.dumps(results, indent=2) + '\n')


if __name__ == '__main__':
    main()
