"""Generate inert mutation controls and check the saved Atomscan reports.

Usage: python3 check.py prepare SAMPLE OUTDIR
       atomscan --no-update --follow=none --mode slow -f json OUTDIR > controls.jsonl
       python3 check.py check controls.jsonl
No sample or control is executed.
"""
import json
import pathlib
import sys

PREFIX = 'objectives/impact/dos/attack/botnet::x86-64-framed-udp-flood'
BOT = 'objectives/command-and-control/botnet/iot::static-x86-64-procfs-syscall-bot'
RETIRED = {
    'objectives/evasion/masquerade/identity/daemon::multi-daemon-backdoor',
    'objectives/evasion/masquerade/identity/daemon::fake-crond',
    'objectives/evasion/masquerade/identity/daemon::fake-sshd',
    'objectives/evasion/masquerade/process/system-name::fake-cron-foreground-path',
    'objectives/anti-static/obfuscation/encoding/base64::base64-systemd-path',
}

if sys.argv[1] == 'prepare':
    data = pathlib.Path(sys.argv[2]).read_bytes()
    out = pathlib.Path(sys.argv[3]); out.mkdir(parents=True, exist_ok=True)
    (out / 'positive.elf').write_bytes(data)
    for name, offset in {
        'parser-call-redirected': 0x5ba2,
        'receive-call-redirected': 0x5b37,
        'send-call-redirected': 0x336d,
        'receive-syscall-changed': 0xb460,
        'outer-repeat-branch-changed': 0x3375,
    }.items():
        changed = bytearray(data); changed[offset] ^= 1
        (out / (name + '.elf')).write_bytes(changed)
    # A structural near miss retaining static uClibc, paths, credential data,
    # and generic socket/kill syscalls, without any application code.
    changed = bytearray(data)
    changed[0x100:0xed76] = b'\x90' * (0xed76 - 0x100)
    for start, end in [(0x9188, 0x91b4), (0xb4fc, 0xb530)]:
        changed[start:end] = data[start:end]
    (out / 'generic-static-paths-syscalls.elf').write_bytes(changed)
elif sys.argv[1] == 'check':
    results = []
    for line in pathlib.Path(sys.argv[2]).read_text().splitlines():
        report = json.loads(line)
        f = report['raw']['files'][0]
        name = pathlib.Path(f['path']).name
        ids = {t['id'] for t in f.get('traits', [])}
        assert not ids & RETIRED, (name, ids & RETIRED)
        # Skipping REX.W narrows a save but still executes the parser.
        # Skipping the optional body peek also preserves body reception.
        expected = name in {'positive.elf', 'parser-call-redirected.elf',
                            'receive-call-redirected.elf'}
        assert (PREFIX in ids) == expected, name
        assert (BOT in ids) == expected, name
        results.append({'control': name, 'flood': PREFIX in ids, 'bot': BOT in ids})
    assert len(results) == 7, len(results)
    print(json.dumps(results, indent=2))
else:
    raise SystemExit('expected prepare or check')
